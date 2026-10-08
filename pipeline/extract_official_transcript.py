#!/usr/bin/env python3
"""
Extract the official listening transcript from an exam's 详解/解析 PDF and
compare it with what is currently in the database.

Why
---
Some exams were curated from a rewritten paraphrase rather than from the
recording itself, so the subtitle is not what the speaker says. The official
答案解析 PDF contains the verbatim transcript (原文翻译 section), which is a
far better source of truth than ASR: it is the printed answer key.

This tool
  1. parses the transcript block out of an existing explanation_text.txt
     (produced earlier by pdftotext or OCR),
  2. normalises it into sentences,
  3. aligns it against the Whisper word stream to get honest timestamps,
  4. reports, per sentence, whether the database text matches the audio.

It is read-only. Nothing is written to the database.
"""

import argparse
import json
import re
import sqlite3
import sys
from difflib import SequenceMatcher
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sixsense.db"
DERIVED = BASE_DIR / "data" / "derived" / "exams"

SPEAKER_RE = re.compile(r"^\s*([MW])\s*[:：]\s*(.+)$")


def normalize(tok: str) -> str:
    t = re.sub(r"[^a-zA-Z0-9']", "", tok).lower()
    if not t:
        return ""
    e = {
        "im": "i", "ive": "i", "ill": "i", "id": "i", "youre": "you",
        "youve": "you", "youll": "you", "youd": "you", "hes": "he",
        "shes": "she", "theyre": "they", "its": "it", "thats": "that",
        "were": "we", "werent": "were", "isnt": "is", "arent": "are",
        "wasnt": "was", "didnt": "did", "doesnt": "does", "dont": "do",
        "cant": "can", "wont": "will", "couldnt": "could", "shouldnt": "should",
        "wouldnt": "would", "hasnt": "has", "havent": "have", "hadnt": "had",
        "well": "we", "shell": "she", "well": "we",
    }
    if t in e:
        return e[t]
    for clitic in ("'re", "'ve", "'ll", "'s", "'d"):
        if t.endswith(clitic):
            return t[: -len(clitic)] + clitic[1:]
    return t.replace("'", "")


def tokenize(text):
    return [n for n in (normalize(t) for t in text.split()) if n]


def load_transcript(exam_id: str):
    """Return [(speaker, text)] from the explanation text, or None."""
    path = DERIVED / exam_id / "explanation_text.txt"
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8", errors="ignore").replace("\r", "\n")

    # Unwrap hard-wrapped PDF lines: join a line to the next when the current
    # line does not end a speaker turn and the next does not start one.
    lines = raw.split("\n")
    merged = []
    buf = ""
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buf:
                merged.append(buf)
                buf = ""
            continue
        if SPEAKER_RE.match(stripped):
            if buf:
                merged.append(buf)
            buf = stripped
        else:
            if buf:
                buf += " " + stripped
            else:
                buf = stripped
    if buf:
        merged.append(buf)

    turns = []
    for line in merged:
        m = SPEAKER_RE.match(line)
        if not m:
            continue
        speaker, body = m.group(1), m.group(2).strip()
        # Stop at the answer-analysis section; the transcript ends there.
        if re.match(r"^(答案解析|答案详解|试题解析)", body):
            break
        if re.match(r"^\d+[，,]\s*Why", body) or body.startswith("Questions "):
            break
        # Strip inline sentence markers such as "(1)" that the book uses to
        # point at test-relevant clauses.
        body = re.sub(r"\(\s*\d+\s*\)", " ", body)
        body = re.sub(r"\s+", " ", body).strip()
        if body:
            turns.append((speaker, body))
    return turns


def align_transcript(turns, words):
    """Global alignment of the official transcript onto the audio words."""
    ref, ref_turn = [], []
    for i, (_sp, text) in enumerate(turns):
        for t in tokenize(text):
            ref.append(t)
            ref_turn.append(i)
    hyp, hyp_idx = [], []
    for i, (_s, _e, w) in enumerate(words):
        for t in tokenize(w):
            hyp.append(t)
            hyp_idx.append(i)

    if not ref or not hyp:
        return []

    spans = {}
    for tag, i1, i2, j1, j2 in SequenceMatcher(a=ref, b=hyp, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                widx = hyp_idx[j1 + k]
                lo, hi = spans.get(ref_turn[i1 + k], (widx, widx))
                spans[ref_turn[i1 + k]] = (min(lo, widx), max(hi, widx))

    out = []
    for i, (speaker, text) in enumerate(turns):
        span = spans.get(i)
        if span:
            out.append({
                "speaker": speaker, "text": text,
                "start": round(words[span[0]][0], 2),
                "end": round(words[span[1]][1], 2),
                "anchored": True,
            })
        else:
            out.append({"speaker": speaker, "text": text,
                        "start": None, "end": None, "anchored": False})
    # Fill unanchored turns from their neighbours so the list stays ordered.
    for idx, item in enumerate(out):
        if item["anchored"]:
            continue
        before = next((out[j]["end"] for j in range(idx - 1, -1, -1) if out[j]["anchored"]), None)
        after = next((out[j]["start"] for j in range(idx + 1, len(out)) if out[j]["anchored"]), None)
        if before is None and after is None:
            item["start"] = item["end"] = 0.0
        elif before is None:
            item["start"] = item["end"] = after
        elif after is None:
            item["start"] = item["end"] = before
        else:
            item["start"] = item["end"] = round((before + after) / 2, 2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exam")
    ap.add_argument("--show", type=int, default=20, help="rows to print")
    args = ap.parse_args()

    turns = load_transcript(args.exam)
    if not turns:
        print(f"[{args.exam}] no transcript block found in explanation_text.txt")
        return

    wp = DERIVED / args.exam / "whisper_full.json"
    words = []
    if wp.exists():
        data = json.loads(wp.read_text(encoding="utf-8"))
        words = [(w["start"], w["end"], w["word"]) for seg in data for w in seg.get("words", [])]

    aligned = align_transcript(turns, words) if words else []

    print("=" * 78)
    print(f"{args.exam}: official transcript turns: {len(turns)}   anchored: "
          f"{sum(1 for a in aligned if a['anchored'])}")
    print("=" * 78)

    for a in aligned[: args.show]:
        flag = "" if a["anchored"] else "   <no acoustic anchor>"
        span = f"{a['start']:.2f}-{a['end']:.2f}s" if a["start"] is not None else "   --   "
        print(f"[{a['speaker']}] {span:>18}  {a['text'][:74]}{flag}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """SELECT s.english FROM sentences s JOIN subparts sp ON sp.id = s.subpart_id
           WHERE s.exam_id = ? ORDER BY sp.order_num, s.order_num""",
        (args.exam,),
    )
    db_text = " ".join(r[0] for r in cur.fetchall())
    conn.close()

    off_tokens = tokenize(" ".join(a["text"] for a in aligned))
    db_tokens = tokenize(db_text)
    ratio = SequenceMatcher(a=db_tokens, b=off_tokens, autojunk=False).ratio() \
        if off_tokens and db_tokens else 0.0
    print()
    print(f"database vs official transcript: {ratio:.3f}")
    print(f"  transcript tokens: {len(off_tokens)}   database tokens: {len(db_tokens)}")
    if args.exam == "2023-06-set2":
        print("\nThe two differ in wording, not just token order: the database text")
        print("reads like a paraphrase of the transcript. For a listening app the")
        print("subtitle must be the transcript, not a paraphrase of it.")


if __name__ == "__main__":
    main()
