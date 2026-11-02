#!/usr/bin/env python3
"""
scripts/build_vocab_freq.py
Builds CET-6 listening word frequency table from real exam corpus (6,416 sentences across 43 exams).
Stores data into SQLite table `vocab_frequency` and outputs `data/cet6_vocab_freq.json`.
"""

import sqlite3
import re
import json
import time
import os
import sys
from pathlib import Path
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sixsense.db")
JSON_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "data", "cet6_vocab_freq.json")

# Core function / stop words to filter out so frequency focuses on meaningful CET-4/6 vocabulary
STOPWORDS = set("""
a about above across after afterwards again against all almost alone along already also although always am among amongst an and another any anyhow anyone anything anyway anywhere are aren't around as at be became because become becomes becoming been before beforehand behind being below beside besides between beyond both but by can cannot can't could couldn't did didn't do does doesn't doing don't done down during each eg either else elsewhere enough etc even ever every everyone everything everywhere except few for former formerly from further get gets getting give gives giving go goes going gone got had hadn't has hasn't have haven't having he he'd he'll he's hence her here here's hers herself him himself his how how's however i i'd i'll i'm i've if in into is isn't it it's its itself just know knows knowing knew let let's like look looks looking looked made make makes making many may maybe me meantime meanwhile might mine more moreover most mostly much must mustn't my myself name neither never nevertheless next no nobody none noone nor not nothing now nowhere of off often on once one only onto or other others otherwise ought our ours ourselves out over own per perhaps quite rather really right said same say saying says see seeing seen saw shall she she'd she'll she's should shouldn't since so some somehow someone something sometime sometimes somewhere still such than that that's the their theirs them themselves then thence there there's thereafter thereby therefore therein thereupon these they they'd they'll they're they've this those though through throughout thru thus to together too toward towards under until unto up upon us use used uses using very via was wasn't way we we'd we'll we're we've well were weren't what what's whatever when when's whence whenever where where's whereafter whereas whereby wherein whereupon wherever whether which while whither who who's whoever whole whom whose why why's will with within without won't would wouldn't yes yet you you'd you'll you're you've your yours yourself yourselves yeah oh okay ok uh um ah mm wow hello hi hey bye mr mrs ms dr don ve ll re d m t s
""".split())

def clean_definition(pos: str, meaning: str) -> str:
    """Keep concise 1-line definition suitable for mobile flashcard (avoid clutter)."""
    if not meaning:
        return ""
    # Split by semicolon and keep top 2 items
    parts = [p.strip() for p in re.split(r"[；;]", meaning) if p.strip()]
    concise = "；".join(parts[:2]) if parts else meaning
    return f"{pos} {concise}".strip() if pos else concise

def query_dict_fallback(word: str):
    """Query Youdao dictionary for definition and phonetics."""
    from backend.app.routers.dict import query_youdao
    try:
        data = query_youdao(word)
        if not data:
            return None
        uk_phone = data.get("phonetic_uk") or ""
        us_phone = data.get("phonetic_us") or ""
        phone = us_phone or uk_phone or ""
        defs = data.get("definitions") or []
        pos = defs[0].get("pos", "") if defs else ""
        meaning = defs[0].get("meaning", "") if defs else ""
        clean_def = clean_definition(pos, meaning)
        tags = data.get("tags") or []
        return {
            "phonetic": phone,
            "phonetic_uk": uk_phone,
            "phonetic_us": us_phone,
            "pos": pos,
            "definition_zh": clean_def,
            "tags": tags,
        }
    except Exception as e:
        return None

def build():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Ensure tables exist
    c.execute("""
    CREATE TABLE IF NOT EXISTS vocab_frequency (
        word TEXT PRIMARY KEY,
        frequency INTEGER NOT NULL DEFAULT 1,
        exam_count INTEGER NOT NULL DEFAULT 1,
        phonetic TEXT DEFAULT '',
        phonetic_uk TEXT DEFAULT '',
        phonetic_us TEXT DEFAULT '',
        pos TEXT DEFAULT '',
        definition_zh TEXT DEFAULT '',
        tags_json TEXT DEFAULT '[]',
        examples_json TEXT DEFAULT '[]'
    );
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_vocab_freq_count ON vocab_frequency(frequency DESC);")

    c.execute("""
    CREATE TABLE IF NOT EXISTS user_vocab_status (
        user_id TEXT NOT NULL,
        word TEXT NOT NULL,
        status TEXT NOT NULL,
        updated_at REAL NOT NULL,
        PRIMARY KEY (user_id, word)
    );
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_user_vocab_status ON user_vocab_status(user_id, status);")
    conn.commit()

    # 2. Extract corpus sentences
    print("Reading sentences from database...")
    rows = c.execute("""
        SELECT s.id, s.exam_id, s.start_time, s.end_time, s.english, s.chinese, e.audio_file
        FROM sentences s
        JOIN exams e ON s.exam_id = e.id
        ORDER BY s.order_num ASC
    """).fetchall()
    print(f"Loaded {len(rows)} sentences.")

    word_counts = Counter()
    word_exams = defaultdict(set)
    word_sentences = defaultdict(list)

    for sid, eid, st, et, en, zh, audio in rows:
        tokens = re.findall(r"[a-zA-Z]+", en.lower())
        seen_in_sent = set()
        for t in tokens:
            if len(t) <= 2 or t in STOPWORDS:
                continue
            word_counts[t] += 1
            word_exams[t].add(eid)
            if t not in seen_in_sent:
                seen_in_sent.add(t)
                if len(word_sentences[t]) < 8:  # Store up to 8 real exam occurrences
                    word_sentences[t].append({
                        "sentence_id": sid,
                        "exam_id": eid,
                        "audio_file": audio,
                        "start_time": round(st, 2),
                        "end_time": round(et, 2),
                        "english": en,
                        "chinese": zh
                    })

    # Filter words appearing at least twice
    frequent_words = [w for w, cnt in word_counts.most_common() if cnt >= 2]
    print(f"Total words with frequency >= 2: {len(frequent_words)}")

    # 3. Load existing cached definitions from dictionary_cache and vocab_frequency
    cached_dict = {}
    for r in c.execute("SELECT word, data_json FROM dictionary_cache").fetchall():
        try:
            d = json.loads(r[1])
            uk = d.get("phonetic_uk", "")
            us = d.get("phonetic_us", "")
            defs = d.get("definitions", [])
            pos = defs[0].get("pos", "") if defs else ""
            m = defs[0].get("meaning", "") if defs else ""
            cached_dict[r[0]] = {
                "phonetic": us or uk or "",
                "phonetic_uk": uk,
                "phonetic_us": us,
                "pos": pos,
                "definition_zh": clean_definition(pos, m),
                "tags": d.get("tags", []),
            }
        except Exception:
            pass

    for r in c.execute("SELECT word, phonetic, phonetic_uk, phonetic_us, pos, definition_zh, tags_json FROM vocab_frequency").fetchall():
        if r[5]: # has definition
            cached_dict[r[0]] = {
                "phonetic": r[1],
                "phonetic_uk": r[2],
                "phonetic_us": r[3],
                "pos": r[4],
                "definition_zh": r[5],
                "tags": json.loads(r[6] or "[]"),
            }

    print(f"Existing cached definitions: {len(cached_dict)}")

    # 4. Fetch definitions for top high-frequency words that are missing (e.g. top 100)
    top_target = frequent_words[:100]
    missing = [w for w in top_target if w not in cached_dict]
    print(f"Missing definitions in top 100: {len(missing)}")

    if missing:
        print(f"Fetching {len(missing)} missing definitions concurrently...")
        def fetch_w(w):
            res = query_dict_fallback(w)
            return w, res

        with ThreadPoolExecutor(max_workers=8) as ex:
            results = ex.map(fetch_w, missing)
            for w, res in results:
                if res:
                    cached_dict[w] = res

    # 5. Insert / Update into vocab_frequency table
    print("Saving to database...")
    items_to_save = []
    json_export = []

    for w in frequent_words:
        cnt = word_counts[w]
        ex_cnt = len(word_exams[w])
        ex_json = json.dumps(word_sentences[w], ensure_ascii=False)
        d_info = cached_dict.get(w, {})
        phonetic = d_info.get("phonetic", "")
        p_uk = d_info.get("phonetic_uk", "")
        p_us = d_info.get("phonetic_us", "")
        pos = d_info.get("pos", "")
        definition = d_info.get("definition_zh", "")
        tags = json.dumps(d_info.get("tags", []), ensure_ascii=False)

        items_to_save.append((
            w, cnt, ex_cnt, phonetic, p_uk, p_us, pos, definition, tags, ex_json
        ))

        json_export.append({
            "word": w,
            "frequency": cnt,
            "exam_count": ex_cnt,
            "phonetic": phonetic,
            "phonetic_uk": p_uk,
            "phonetic_us": p_us,
            "pos": pos,
            "definition_zh": definition,
            "example_count": len(word_sentences[w]),
            "examples": word_sentences[w]
        })

    c.executemany("""
    INSERT INTO vocab_frequency (
        word, frequency, exam_count, phonetic, phonetic_uk, phonetic_us, pos, definition_zh, tags_json, examples_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(word) DO UPDATE SET
        frequency=excluded.frequency,
        exam_count=excluded.exam_count,
        phonetic=CASE WHEN excluded.phonetic != '' THEN excluded.phonetic ELSE vocab_frequency.phonetic END,
        phonetic_uk=CASE WHEN excluded.phonetic_uk != '' THEN excluded.phonetic_uk ELSE vocab_frequency.phonetic_uk END,
        phonetic_us=CASE WHEN excluded.phonetic_us != '' THEN excluded.phonetic_us ELSE vocab_frequency.phonetic_us END,
        pos=CASE WHEN excluded.pos != '' THEN excluded.pos ELSE vocab_frequency.pos END,
        definition_zh=CASE WHEN excluded.definition_zh != '' THEN excluded.definition_zh ELSE vocab_frequency.definition_zh END,
        tags_json=CASE WHEN excluded.tags_json != '[]' THEN excluded.tags_json ELSE vocab_frequency.tags_json END,
        examples_json=excluded.examples_json;
    """, items_to_save)

    conn.commit()
    conn.close()

    # Save JSON manifest
    with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(json_export, f, ensure_ascii=False, indent=2)

    print(f"Successfully processed {len(items_to_save)} vocabulary items.")
    print(f"Saved to DB: {DB_PATH}")
    print(f"Saved to JSON: {JSON_OUTPUT}")

if __name__ == "__main__":
    build()
