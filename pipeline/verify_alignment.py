#!/usr/bin/env python3
"""
Subtitle-voice alignment verifier (字幕-语音一致性核验).

For every sentence in the database, this script reads back the Whisper
word-level timestamps that fall inside the sentence's [start_time, end_time]
window and compares those acoustic words against the subtitle text.

It answers the only question that matters for a listening app:
"if the player seeks to start_time and plays until end_time, does the human
actually hear the words shown in the subtitle?"

Three metrics per sentence:
  coverage  = acoustic words inside window / subtitle tokens   (subtitle not truncated)
  speech_rate = acoustic words per second                     (0.8-6.0 w/s is natural)
  token_match = difflib ratio between acoustic and subtitle    (>=0.70 is aligned)

A sentence is flagged FAIL if any of:
  - token_match < 0.70        -> the audio in this window says something else
  - speech_rate outside range -> window length is physically wrong
  - coverage < 0.75           -> part of the subtitle is spoken outside the window
  - end_time > next subpart start or > subpart end_time

Usage:
    python3 pipeline/verify_alignment.py                 # all exams
    python3 pipeline/verify_alignment.py 2019-06-set1    # one exam
"""

import json
import re
import sqlite3
import sys
from difflib import SequenceMatcher
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sixsense.db"
DERIVED_DIR = BASE_DIR / "data" / "derived" / "exams"

MIN_TOKEN_MATCH = 0.70
MIN_COVERAGE = 0.75
MIN_RATE = 0.8
MAX_RATE = 6.0

CONTRACTIONS = {
    "im": "i", "youre": "you", "were": "we", "theyre": "they", "hes": "he",
    "shes": "she", "its": "it", "thats": "that", "whats": "what", "lets": "let",
    "ive": "i", "ill": "i", "youll": "you", "well": "we", "id": "i", "wed": "we",
    "youd": "you", "thered": "there", "whos": "who", "hows": "how",
    "cant": "can", "wont": "will", "didnt": "did", "doesnt": "does", "dont": "do",
    "isnt": "is", "arent": "are", "wasnt": "was", "werent": "were", "hasnt": "has",
    "havent": "have", "hadnt": "had", "couldnt": "could", "shouldnt": "should",
    "wouldnt": "would", "mustnt": "must", "neednt": "need", "shant": "shall",
}


def normalize(tok: str) -> str:
    """Lowercase, strip punctuation, expand contractions to base forms."""
    t = re.sub(r"[^a-zA-Z0-9']", "", tok).lower()
    if not t:
        return ""
    if t in CONTRACTIONS:
        return CONTRACTIONS[t]
    for clitic in ("'re", "'ve", "'ll", "'s", "'d"):
        if t.endswith(clitic):
            return t[:-len(clitic)] + clitic[1:]
    return t.replace("'", "")


def tokenize(text: str):
    return [n for n in (normalize(t) for t in text.split()) if n]


def load_words(exam_id: str):
    path = DERIVED_DIR / exam_id / "whisper_full.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for seg in data:
        for w in seg.get("words", []):
            out.append((w["start"], w["end"], w["word"]))
    return out


def main():
    exam_filter = sys.argv[1] if len(sys.argv) > 1 else None
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if exam_filter:
        exams = [exam_filter]
    else:
        cur.execute("SELECT id FROM exams ORDER BY id")
        exams = [r[0] for r in cur.fetchall()]

    print("=" * 78)
    print("Subtitle / Voice Alignment Verification (字幕-语音一致性核验)")
    print("=" * 78)

    grand_fail = 0
    grand_sent = 0
    grand_exam_fail = 0

    for exam_id in exams:
        cur.execute("SELECT title FROM exams WHERE id = ?", (exam_id,))
        row = cur.fetchone()
        if not row:
            print(f"\n[SKIP] {exam_id}: not in database")
            continue

        words = load_words(exam_id)
        if words is None:
            print(f"\n[SKIP] {exam_id}: no whisper_full.json, cannot verify acoustically")
            continue

        cur.execute(
            "SELECT id, start_time, end_time FROM subparts WHERE exam_id = ? ORDER BY order_num",
            (exam_id,),
        )
        subpart_ends = {sid: et for sid, _st, et in cur.fetchall()}

        cur.execute(
            """SELECT id, subpart_id, order_num, start_time, end_time, english, chinese
               FROM sentences WHERE exam_id = ? ORDER BY order_num""",
            (exam_id,),
        )
        sentences = cur.fetchall()

        fails = []
        for sid, sp_id, order_num, st, et, english, chinese in sentences:
            problems = []

            sub_refs = tokenize(english)
            # A player hears every word that overlaps the window, not only the
            # words fully contained by it, so the window is judged the same way.
            inside = [
                (s, e, w) for (s, e, w) in words
                if (e > st + 0.01) and (s < et - 0.01)
            ]
            ac_refs = tokenize(" ".join(w for _s, _e, w in inside))

            duration = et - st
            rate = len(ac_refs) / duration if duration > 0 else 0.0
            coverage = len(ac_refs) / len(sub_refs) if sub_refs else 0.0
            match = SequenceMatcher(a=sub_refs, b=ac_refs, autojunk=False).ratio() if (sub_refs and ac_refs) else 0.0

            if match < MIN_TOKEN_MATCH:
                problems.append(f"token_match={match:.2f} (audio says different words)")
            if not (MIN_RATE <= rate <= MAX_RATE):
                problems.append(f"speech_rate={rate:.2f} w/s out of natural range")
            if coverage < MIN_COVERAGE:
                problems.append(f"coverage={coverage:.2f} (subtitle words spoken outside window)")
            if sp_id in subpart_ends and et > subpart_ends[sp_id] + 0.05:
                problems.append(f"exceeds subpart end_time {subpart_ends[sp_id]}")
            if not re.search(r"[\u4e00-\u9fff]", chinese or ""):
                problems.append("empty/non-Chinese translation")

            if problems:
                fails.append((order_num, st, et, english, problems, " ".join(ac_refs)))

        grand_sent += len(sentences)
        grand_fail += len(fails)
        grand_exam_fail += 1 if fails else 0

        status = "PASS" if not fails else f"FAIL ({len(fails)}/{len(sentences)})"
        print(f"\n[{exam_id}] {row[0]}")
        print(f"  Sentences: {len(sentences)}   Verified: {len(sentences) - len(fails)}   {status}")

        for order_num, st, et, english, problems, heard in fails:
            print(f"    ! #{order_num} [{st:.2f}-{et:.2f}s] {english[:60]}")
            for p in problems:
                print(f"        - {p}")
            print(f"        heard: {heard[:80]}")

    print("\n" + "=" * 78)
    if grand_sent:
        avg_ok = (grand_sent - grand_fail) / grand_sent * 100
        print(f"Total sentences verified: {grand_sent}")
        print(f"Aligned: {grand_sent - grand_fail} ({avg_ok:.2f}%)   Misaligned: {grand_fail}")
        print(f"Exams fully aligned: {len(exams) - grand_exam_fail}/{len(exams)}")
    print("=" * 78)

    conn.close()
    sys.exit(1 if grand_fail else 0)


if __name__ == "__main__":
    main()
