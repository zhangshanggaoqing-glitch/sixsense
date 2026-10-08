#!/usr/bin/env python3
"""
Export per-sentence audio clips so a human can verify subtitle/voice pairing
by ear (人工抽听核验).

For each sentence this writes a short mp3 covering exactly [start_time,
end_time] plus a small lead-in/lead-out, and a manifest listing the clip file
next to its English and Chinese subtitle. Listening to the clips in order tells
you immediately whether the player would show the right words at the right
moment.

Nothing here trusts the database. The clip boundaries come from the sentence
timestamps, and the manifest text is printed from the same row, so if a
timestamp is wrong you hear the mismatch yourself.

Examples
--------
    # every flagged sentence of every exam (what the verifier suspects)
    python3 pipeline/export_check_clips.py --flagged-only

    # one exam, one subpart, first 20 sentences
    python3 pipeline/export_check_clips.py 2023-06-set2 --subpart conv-1 --limit 20

    # a random spread across an exam, as an unbiased spot check
    python3 pipeline/export_check_clips.py 2025-12-set1 --sample 15
"""

import argparse
import json
import random
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sixsense.db"
OUT_ROOT = BASE_DIR / "data" / "qa_clips"
RAW_ROOT = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频")
DERIVED_DIR = BASE_DIR / "data" / "derived" / "exams"

LEAD_IN = 0.30
LEAD_OUT = 0.30


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
    }
    if t in e:
        return e[t]
    for clitic in ("'re", "'ve", "'ll", "'s", "'d"):
        if t.endswith(clitic):
            return t[: -len(clitic)] + clitic[1:]
    return t.replace("'", "")


def tokenize(text):
    return [n for n in (normalize(t) for t in text.split()) if n]


def resolve_audio(audio_file: str):
    hits = list(RAW_ROOT.rglob(audio_file))
    return hits[0] if hits else None


def flagged_sentence_ids():
    """Re-run the alignment check and return the sentence ids it flags."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import verify_alignment as va

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM exams ORDER BY id")
    exams = [r[0] for r in cur.fetchall()]
    conn.close()

    flagged = set()
    for exam_id in exams:
        words = va.load_words(exam_id)
        if words is None:
            continue
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            """SELECT s.id, s.start_time, s.end_time, s.english
               FROM sentences s WHERE s.exam_id = ? ORDER BY s.order_num""",
            (exam_id,),
        )
        for sid, st, et, en in cur.fetchall():
            inside = [w for (s, e, w) in words if (e > st + 0.01) and (s < et - 0.01)]
            ac = tokenize(" ".join(inside))
            ref = tokenize(en)
            if not ref or not ac:
                flagged.add(sid)
                continue
            rate = len(ac) / (et - st) if et > st else 0
            cov = len(ac) / len(ref)
            from difflib import SequenceMatcher
            m = SequenceMatcher(a=ref, b=ac, autojunk=False).ratio()
            if m < va.MIN_TOKEN_MATCH or cov < va.MIN_COVERAGE or not (0.8 <= rate <= 6.0):
                flagged.add(sid)
        conn.close()
    return flagged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exam", nargs="?", help="exam id; default is all exams")
    ap.add_argument("--flagged-only", action="store_true",
                    help="only export sentences the alignment verifier flags")
    ap.add_argument("--subpart", help="limit to one subpart, e.g. conv-1 or rec-3")
    ap.add_argument("--limit", type=int, help="max sentences per exam")
    ap.add_argument("--sample", type=int, help="export N randomly chosen sentences")
    ap.add_argument("--list", action="store_true",
                    help="print the clip manifest paths only, cut nothing")
    args = ap.parse_args()

    flagged = flagged_sentence_ids() if args.flagged_only else None

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if args.exam:
        exams = [args.exam]
    else:
        cur.execute("SELECT id FROM exams ORDER BY id")
        exams = [r[0] for r in cur.fetchall()]

    total = 0
    for exam_id in exams:
        cur.execute("SELECT audio_file FROM exams WHERE id = ?", (exam_id,))
        row = cur.fetchone()
        if not row:
            continue

        sql = """SELECT s.id, s.order_num, s.speaker, s.start_time, s.end_time,
                        s.english, s.chinese, s.subpart_id
                 FROM sentences s
                 JOIN subparts sp ON sp.id = s.subpart_id
                 WHERE s.exam_id = ?"""
        params = [exam_id]
        if args.subpart:
            sql += " AND s.subpart_id LIKE ?"
            params.append(f"%{args.subpart}")
        sql += " ORDER BY sp.order_num, s.order_num"
        rows = cur.execute(sql, params).fetchall()
        rows = [(r[0], r[1], r[2], r[3], r[4], r[5], r[6],
                 "-".join(r[7].split("-")[-2:]))
                for r in rows]

        if flagged is not None:
            rows = [r for r in rows if r[0] in flagged]
        if args.sample and args.sample < len(rows):
            rows = random.Random(42).sample(rows, args.sample)
        if args.limit:
            rows = rows[: args.limit]
        if not rows:
            continue

        out_dir = OUT_ROOT / exam_id
        out_dir.mkdir(parents=True, exist_ok=True)

        if args.list:
            print(f"\n{exam_id}: {len(rows)} sentences would be exported to {out_dir}")
            continue

        if flagged is None:
            src = resolve_audio(row[0])
            if src is None:
                print(f"[{exam_id}] audio not found: {row[0]}")
                continue
        else:
            src = resolve_audio(row[0]) or resolve_audio(
                cur.execute("SELECT audio_file FROM exams WHERE id=?", (exam_id,)).fetchone()[0])

        manifest = [
            f"# {exam_id}  subtitle/voice spot-check clips",
            f"# audio: {src.name if src else 'NOT FOUND'}",
            f"# lead-in {LEAD_IN}s, lead-out {LEAD_OUT}s",
            "",
        ]
        for sid, order_num, speaker, st, et, en, zh, code in rows:
            clip = out_dir / f"{code}-{order_num:04d}.mp3"
            start = max(0.0, st - LEAD_IN)
            dur = (et - st) + LEAD_IN + LEAD_OUT
            cmd = ["ffmpeg", "-y", "-loglevel", "error",
                   "-ss", f"{start:.2f}", "-t", f"{dur:.2f}",
                   "-i", str(src), "-ac", "1", "-ar", "22050", "-b:a", "48k",
                   str(clip)]
            subprocess.run(cmd, check=False)
            total += 1
            manifest += [
                f"[{clip.name}]  {st:.2f}-{et:.2f}s  ({speaker}, {code})"
                + ("   <== FLAGGED" if flagged and sid in flagged else ""),
                f"  EN: {en}",
                f"  ZH: {zh}",
                "",
            ]

        (out_dir / "manifest.txt").write_text("\n".join(manifest), encoding="utf-8")
        print(f"[{exam_id}] exported {len(rows)} clips -> {out_dir}")

    conn.close()
    if not args.list:
        print(f"\nTotal clips: {total}")
        print("Listen in order with:  ffplay -autoexit -nodisp <file>.mp3")
        print("Or play a whole exam:  mpv --playlist=data/qa_clips/<exam>/manifest.txt 2>/dev/null || "
              "for f in data/qa_clips/<exam>/*.mp3; do ffplay -autoexit -nodisp -v error \"$f\"; done")


if __name__ == "__main__":
    main()
