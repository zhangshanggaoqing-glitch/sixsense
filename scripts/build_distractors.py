#!/usr/bin/env python3
"""
scripts/build_distractors.py
Precomputes 3 listening distractors for each CET-6 vocabulary word.
Uses length bucketing, Levenshtein distance, acoustic soundex, and frequency proximity,
while strictly filtering out morphological/root variants of the target word.
Stores results in SQLite table `vocab_distractors` and `data/cet6_distractors.json`.
"""

import sqlite3
import json
import math
import os
from collections import defaultdict

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sixsense.db")
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), "..", "data", "cet6_distractors.json")

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def get_stem(w):
    suffixes = (
        'ing', 'ed', 'ers', 'er', 'es', 's', 'al', 'ment', 'ments',
        'tion', 'tions', 'sion', 'sions', 'ly', 'able', 'ible',
        'ive', 'ity', 'ize', 'ise', 'ant', 'ants', 'ent', 'ents',
        'ated', 'ating', 'ation', 'ations', 'ful', 'less', 'ness'
    )
    curr = w.lower()
    changed = True
    while changed:
        changed = False
        for suf in suffixes:
            if curr.endswith(suf) and len(curr) - len(suf) >= 3:
                curr = curr[:-len(suf)]
                changed = True
                break
    return curr

def are_same_root(w1, w2):
    if w1 == w2:
        return True
    # Direct inflections: -s, -es, -d, -ed, -ing, -er, -est
    for suf in ('s', 'es', 'd', 'ed', 'ing', 'er', 'est', 'ly'):
        if w1 + suf == w2 or w2 + suf == w1:
            return True
    st1 = get_stem(w1)
    st2 = get_stem(w2)
    if st1 == st2 or st1.rstrip('e') == st2.rstrip('e'):
        return True
    min_len = min(len(st1), len(st2))
    if min_len >= 3 and (st1.startswith(st2) or st2.startswith(st1)):
        return True
    return False

def soundex_simple(s):
    s = s.upper()
    if not s: return ""
    first = s[0]
    mapping = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }
    encoded = [first]
    prev = mapping.get(first, '')
    for char in s[1:]:
        code = mapping.get(char, '')
        if code:
            if code != prev:
                encoded.append(code)
            prev = code
        else:
            prev = ''
    result = "".join(encoded)
    return (result + "0000")[:4]

def build():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS vocab_distractors (
        word TEXT PRIMARY KEY,
        distractors_json TEXT NOT NULL,
        quality TEXT NOT NULL
    );
    """)

    rows = c.execute("""
        SELECT word, frequency, pos, phonetic, definition_zh
        FROM vocab_frequency
        ORDER BY frequency DESC;
    """).fetchall()

    print(f"Loaded {len(rows)} words from vocab_frequency.")

    word_pool = []
    by_len = defaultdict(list)

    for r in rows:
        w = r[0].strip().lower()
        if len(w) < 2: continue
        info = {
            "word": w,
            "freq": r[1],
            "pos": r[2] or "",
            "phone": r[3] or "",
            "def": r[4] or "",
            "stem": get_stem(w),
            "soundex": soundex_simple(w),
            "len": len(w),
            "log_freq": math.log(max(1, r[1]))
        }
        word_pool.append(info)
        by_len[len(w)].append(info)

    distractor_map = {}
    db_records = []

    for idx, target in enumerate(word_pool):
        tw = target["word"]
        t_freq = target["freq"]
        t_log_freq = target["log_freq"]
        t_pos = target["pos"]
        t_soundex = target["soundex"]
        t_len = target["len"]

        # Only compare with words in length bucket [t_len - 2, t_len + 2]
        candidate_subset = []
        for l in range(max(2, t_len - 2), t_len + 3):
            candidate_subset.extend(by_len[l])

        scored = []
        for other in candidate_subset:
            ow = other["word"]
            if ow == tw: continue
            if are_same_root(tw, ow): continue

            # Frequency constraint (log difference <= 3.2)
            freq_diff = abs(t_log_freq - other["log_freq"])
            if freq_diff > 3.2: continue

            # Levenshtein distance
            lev = levenshtein(tw, ow)
            max_l = max(t_len, other["len"])
            if lev > max_l - 1: continue  # Skip if completely dissimilar

            edit_sim = 1.0 - (lev / max_l)

            # Acoustic / Soundex similarity
            sound_bonus = 0.35 if t_soundex == other["soundex"] else 0.0

            # Prefix / Suffix match
            pref_bonus = 0.25 if t_len >= 3 and ow.startswith(tw[:3]) else 0.0
            suff_bonus = 0.25 if t_len >= 3 and ow.endswith(tw[-3:]) else 0.0

            # POS match
            pos_bonus = 0.15 if t_pos and other["pos"] and t_pos == other["pos"] else 0.0

            score = (edit_sim * 1.6) + sound_bonus + pref_bonus + suff_bonus + pos_bonus - (freq_diff * 0.04)
            scored.append((ow, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        chosen = []
        for cand, score in scored:
            if cand not in chosen and not any(are_same_root(cand, ex) for ex in chosen):
                chosen.append(cand)
            if len(chosen) == 3:
                break

        # Fallback if fewer than 3
        quality = "high"
        if len(chosen) < 3:
            quality = "fallback"
            for other in candidate_subset:
                ow = other["word"]
                if ow != tw and ow not in chosen and not are_same_root(tw, ow):
                    chosen.append(ow)
                if len(chosen) == 3:
                    break

        distractor_map[tw] = {
            "distractors": chosen,
            "quality": quality
        }
        db_records.append((tw, json.dumps(chosen, ensure_ascii=False), quality))

        if (idx + 1) % 1000 == 0 or idx == len(word_pool) - 1:
            print(f"Processed {idx + 1} / {len(word_pool)} words...")

    c.executemany("""
        INSERT INTO vocab_distractors (word, distractors_json, quality)
        VALUES (?, ?, ?)
        ON CONFLICT(word) DO UPDATE SET
            distractors_json = excluded.distractors_json,
            quality = excluded.quality;
    """, db_records)
    conn.commit()
    conn.close()

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(distractor_map, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(db_records)} distractor mappings into DB & {OUTPUT_JSON}.")

if __name__ == "__main__":
    build()
