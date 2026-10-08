#!/usr/bin/env python3
"""
Populate words_json for all 2016 sentences from whisper_full.json.
"""

import sqlite3
import json
import re

DB_PATH = "data/sixsense.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

exams = ["2016-06-set1", "2016-06-set2", "2016-12-set1", "2016-12-set2"]

for eid in exams:
    with open(f"data/derived/exams/{eid}/whisper_full.json") as f:
        w_data = json.load(f)
    whisper_words = [w for seg in w_data for w in seg.get('words', [])]

    c.execute("SELECT id, start_time, end_time, english, words_json FROM sentences WHERE exam_id = ? ORDER BY order_num", (eid,))
    sents = c.fetchall()

    updated = 0
    for sid, st, et, en, wjson in sents:
        # If words_json is missing or empty or '[]' or 'None'
        needs_update = False
        if not wjson or wjson in ('None', 'null', '[]', ''):
            needs_update = True
        else:
            try:
                parsed = json.loads(wjson)
                if not parsed or len(parsed) == 0:
                    needs_update = True
            except:
                needs_update = True

        if needs_update:
            raw_words = en.split()
            # words in whisper around st and et
            cand_words = [
                w for w in whisper_words
                if st - 0.5 <= w['start'] and w['end'] <= et + 0.5
            ]

            if cand_words:
                matched = [
                    {
                        "word": w["word"].strip(),
                        "start": round(w["start"], 2),
                        "end": round(w["end"], 2),
                        "score": round(w.get("probability", 1.0), 3)
                    }
                    for w in cand_words
                ]
            else:
                # Fallback interpolation
                cnt = len(raw_words)
                dur = max(0.5, et - st)
                step = dur / max(1, cnt)
                matched = [
                    {
                        "word": w,
                        "start": round(st + i * step, 2),
                        "end": round(st + (i + 1) * step, 2),
                        "score": 1.0
                    }
                    for i, w in enumerate(raw_words)
                ]

            c.execute("UPDATE sentences SET words_json = ? WHERE id = ?", (json.dumps(matched, ensure_ascii=False), sid))
            updated += 1

    print(f"{eid}: updated words_json for {updated}/{len(sents)} sentences.")

conn.commit()
conn.close()
print("All words_json populated successfully!")
