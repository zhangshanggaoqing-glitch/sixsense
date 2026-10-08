#!/usr/bin/env python3
"""
Re-align every sentence in the database against its Whisper word-level audio.

Why this exists
---------------
The original per-sentence aligners anchored each sentence with a local search
(first-token match, then a last-token back-scan). That works when the curated
text and the ASR hypothesis are nearly identical, but it silently drifts when
they are not: contractions, proper nouns and ASR slips make the anchor land on
the wrong occurrence, and the error then compounds for every later sentence.
Some exams drifted by 20-40 seconds, meaning the player seeks to a moment where
a different sentence is being spoken.

The fix is a single global alignment per exam. The reference stream is every
sentence's tokens in playback order (across all subparts); the hypothesis stream
is every Whisper word in order. One difflib pass then yields a one-to-one,
monotonic token mapping, so sentence N's timestamps come from the exact audio
span its own words occupy.

Safety rails
------------
  - Timestamps are derived only from real Whisper word boundaries.
  - Monotonicity is enforced: s_time >= previous sentence's end_time.
  - The 34s single-sentence circuit breaker is preserved.
  - Subpart start/end are recomputed from their own sentences, so subpart
    windows always contain their sentences.
  - Words the ASR dropped are re-anchored by interpolation inside the
    neighbouring matched spans instead of being guessed at.

Usage
-----
    python3 pipeline/realign_exam.py                 # dry run, report only
    python3 pipeline/realign_exam.py --apply         # write to the database
    python3 pipeline/realign_exam.py 2019-06-set1 --apply
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
DERIVED_DIR = BASE_DIR / "data" / "derived" / "exams"

MAX_SENTENCE_SECONDS = 34.0
MAX_SENTENCE_SPAN = 32.0
MIN_SENTENCE_SECONDS = 0.2
MIN_CONFIDENT_MATCH = 0.55


def normalize(tok: str) -> str:
    """Lowercase, drop punctuation, and collapse contractions to base forms so
    that "I'm" and "I am" compare equal during alignment."""
    t = re.sub(r"[^a-zA-Z0-9']", "", tok).lower()
    if not t:
        return ""
    expansions = {
        "im": "i", "ive": "i", "ill": "i", "id": "i", "youre": "you",
        "youll": "you", "youd": "you", "youve": "you", "hes": "he",
        "shes": "she", "theyre": "they", "theyve": "they", "theyll": "they",
        "werent": "were", "were": "we", "its": "it", "thats": "that",
        "whats": "what", "theres": "there", "lets": "let", "hes": "he",
        "whos": "who", "hows": "how", "isnt": "is", "arent": "are",
        "wasnt": "was", "werent": "were", "didnt": "did", "doesnt": "does",
        "dont": "do", "cant": "can", "wont": "will", "couldnt": "could",
        "shouldnt": "should", "wouldnt": "would", "hasnt": "has",
        "havent": "have", "hadnt": "had", "mustnt": "must", "neednt": "need",
        "shant": "shall", "aint": "is", "wanna": "want", "gotta": "got",
    }
    if t in expansions:
        return expansions[t]
    for clitic in ("'re", "'ve", "'ll", "'s", "'d"):
        if t.endswith(clitic):
            return t[: -len(clitic)] + clitic[1:]
    return t.replace("'", "")


def tokenize(text: str):
    return [n for n in (normalize(t) for t in text.split()) if n]


def load_whisper(exam_id: str):
    path = DERIVED_DIR / exam_id / "whisper_full.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    words = []
    for seg in data:
        for w in seg.get("words", []):
            words.append((w["start"], w["end"], w["word"]))
    return words


def align_exam(exam_id: str, verbose: bool = False):
    """Return {sentence_id: (start, end)} for one exam, plus a report."""
    words = load_whisper(exam_id)
    if words is None:
        return None, {"status": "no whisper_full.json"}

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Playback order: subpart order, then sentence order inside the subpart.
    cur.execute(
        """SELECT s.id, s.subpart_id, s.order_num, s.english, sp.order_num
           FROM sentences s
           JOIN subparts sp ON sp.id = s.subpart_id
           WHERE s.exam_id = ?
           ORDER BY sp.order_num, s.order_num""",
        (exam_id,),
    )
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return None, {"status": "no sentences"}

    # Reference token stream, with a map back to each sentence.
    ref_tokens = []
    ref_sentence = []
    for sent_id, _sp, _on, english, _spo in rows:
        for t in tokenize(english):
            ref_tokens.append(t)
            ref_sentence.append(sent_id)

    hyp_tokens = []
    hyp_index = []
    for i, (_s, _e, w) in enumerate(words):
        for t in tokenize(w):
            hyp_tokens.append(t)
            hyp_index.append(i)

    if not ref_tokens or not hyp_tokens:
        return None, {"status": "empty token stream"}

    matcher = SequenceMatcher(a=ref_tokens, b=hyp_tokens, autojunk=False)
    opcodes = matcher.get_opcodes()

    # Map every hypothesis token back to the sentence that owns it.
    spans = {}
    matched_ref = set()
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            for k in range(i2 - i1):
                sent = ref_sentence[i1 + k]
                widx = hyp_index[j1 + k]
                lo, hi = spans.get(sent, (widx, widx))
                spans[sent] = (min(lo, widx), max(hi, widx))
                matched_ref.add(i1 + k)
        elif tag == "replace":
            # The hypothesis says roughly the same thing with different words
            # (proper nouns, ASR slips). Spread the audio span over the
            # sentences it covers, proportional to their token counts.
            owners = []
            for k in range(i1, i2):
                owners.append((ref_sentence[k], k - i1))
            if not owners:
                continue
            n_hyp = j2 - j1
            per = max(1, (i2 - i1) // len(set(o for o, _ in owners)))
            cursor = 0
            seen = []
            for sent, pos in owners:
                if not seen or seen[-1][0] != sent:
                    seen.append([sent, cursor, cursor])
                cursor += per
                seen[-1][2] = min(cursor, n_hyp)
            for sent, ja, jb in seen:
                if jb <= ja:
                    jb = min(ja + 1, n_hyp)
                for jj in range(j1 + ja, j1 + jb):
                    widx = hyp_index[jj]
                    lo, hi = spans.get(sent, (widx, widx))
                    spans[sent] = (min(lo, widx), max(hi, widx))

    # Ordered sentence list with resolved spans; fill gaps by interpolation.
    ordered = []
    prev_hi = None
    for sent_id, sp_id, _on, english, _spo in rows:
        span = spans.get(sent_id)
        ordered.append({"id": sent_id, "subpart": sp_id, "english": english, "span": span})
        if span:
            prev_hi = span[1]

    # Forward pass: sentences with no acoustic anchor sit between their
    # anchored neighbours. Share the silent gap out proportionally to token
    # count, so every sentence still covers real audio.
    n_tokens = [len(tokenize(it["english"])) or 1 for it in ordered]
    for i, item in enumerate(ordered):
        if item["span"]:
            continue
        before = None
        for j in range(i - 1, -1, -1):
            if ordered[j]["span"]:
                before = ordered[j]["span"][1]
                break
        after = None
        for j in range(i + 1, len(ordered)):
            if ordered[j]["span"]:
                after = ordered[j]["span"][0]
                break

        if before is None and after is None:
            item["span"] = (0, 0)
            continue
        if before is None:
            # No earlier anchor: borrow the words just after this sentence.
            item["span"] = (after, after)
            continue
        if after is None:
            item["span"] = (before, before)
            continue

        gap_words = after - before
        run = 1
        group = 0
        while i - group - 1 >= 0 and not ordered[i - group - 1]["span"]:
            group += 1
        ahead = 0
        while i + ahead + 1 < len(ordered) and not ordered[i + ahead + 1]["span"]:
            ahead += 1
        run = group + ahead + 1
        group_tokens = sum(n_tokens[i - group: i + ahead + 1])
        offset = sum(n_tokens[i - group: i])
        lo = before + max(0, int(gap_words * offset / group_tokens))
        hi = before + max(1, int(gap_words * (offset + n_tokens[i]) / group_tokens))
        lo = max(before, min(lo, after))
        hi = max(lo, min(hi, after))
        item["span"] = (lo, hi)

    # Materialize times with monotonicity and the 34s breaker.
    result = {}
    prev_end = None
    stats = {"shifted": 0, "anchored": 0, "interpolated": 0, "capped": 0,
             "max_shift": 0.0, "mean_shift": 0.0}
    anchored_ids = {it["id"] for it in ordered if it["span"]}
    interpolated_ids = {it["id"] for it in ordered if not it["span"]}

    conn = sqlite3.connect(DB_PATH)
    for item in ordered:
        lo, hi = item["span"]
        s_time = round(words[lo][0], 2)
        e_time = round(words[hi][1], 2)

        if prev_end is not None and s_time < prev_end:
            s_time = prev_end
        if e_time < s_time + MIN_SENTENCE_SECONDS:
            e_time = round(s_time + MIN_SENTENCE_SECONDS, 2)

        if e_time - s_time > MAX_SENTENCE_SECONDS:
            e_time = round(s_time + MAX_SENTENCE_SPAN, 2)
            stats["capped"] += 1

        result[item["id"]] = (s_time, e_time)
        prev_end = e_time

    # Measure the correction against what is currently stored.
    shifts = []
    for item in ordered:
        cur = conn.execute("SELECT start_time FROM sentences WHERE id = ?", (item["id"],)).fetchone()
        if cur:
            shifts.append(abs(result[item["id"]][0] - cur[0]))
    conn.close()

    stats["shifted"] = sum(1 for x in shifts if x > 0.5)
    stats["anchored"] = len(anchored_ids)
    stats["interpolated"] = len(interpolated_ids)
    stats["max_shift"] = max(shifts) if shifts else 0.0
    stats["mean_shift"] = sum(shifts) / len(shifts) if shifts else 0.0
    stats["status"] = "ok"
    return result, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exam", nargs="?", help="exam id; default is all exams")
    ap.add_argument("--apply", action="store_true", help="write to the database")
    args = ap.parse_args()

    conn = sqlite3.connect(DB_PATH)
    if args.exam:
        exams = [args.exam]
    else:
        exams = [r[0] for r in conn.execute("SELECT id FROM exams ORDER BY id")]
    conn.close()

    print("=" * 78)
    print("Global re-alignment" + ("  [APPLY]" if args.apply else "  [DRY RUN]"))
    print("=" * 78)
    print(f"{'exam':15} {'sent':>5} {'shifted':>8} {'interp':>7} {'capped':>7} {'max shift':>10} {'mean':>7}")

    updates = {}
    for exam_id in exams:
        result, stats = align_exam(exam_id)
        if result is None:
            print(f"{exam_id:15}  SKIP ({stats['status']})")
            continue
        updates[exam_id] = result
        print(f"{exam_id:15} {len(result):5d} {stats['shifted']:8d} {stats['interpolated']:7d} "
              f"{stats['capped']:7d} {stats['max_shift']:9.2f}s {stats['mean_shift']:6.2f}s")

    if not args.apply:
        print("\nDry run only. Re-run with --apply to write the database.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    written = 0
    for exam_id, mapping in updates.items():
        for sent_id, (s_time, e_time) in mapping.items():
            cur.execute(
                "UPDATE sentences SET start_time = ?, end_time = ? WHERE id = ?",
                (s_time, e_time, sent_id),
            )
            written += 1
        # Recompute subpart windows from the sentences they contain, so a
        # subpart always spans its own content.
        cur.execute(
            """SELECT sp.id, MIN(s.start_time), MAX(s.end_time)
               FROM subparts sp JOIN sentences s ON s.subpart_id = sp.id
               WHERE sp.exam_id = ?
               GROUP BY sp.id ORDER BY sp.order_num""",
            (exam_id,),
        )
        for sp_id, sp_start, sp_end in cur.fetchall():
            cur.execute(
                "UPDATE subparts SET start_time = ?, end_time = ?, duration = ? WHERE id = ?",
                (round(sp_start, 2), round(sp_end, 2), round(sp_end - sp_start, 2), sp_id),
            )
    conn.commit()
    conn.close()
    print(f"\nWrote {written} sentence timestamps.")


if __name__ == "__main__":
    main()
