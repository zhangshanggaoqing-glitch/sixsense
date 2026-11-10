#!/usr/bin/env python3
"""Reproducible isolated benchmark.

This does not open the repository database, the production host, or any user rows.
Numbers are from this machine and a synthetic SQLite file. They are not production latency.
"""

import os
import sqlite3
import statistics
import tempfile
import time
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="sixsense-bench-")
os.environ["SIX_SENSE_DATA_DIR"] = TMP
os.environ["JWT_SECRET"] = "bench-secret"
os.environ["CET6_RAW_SOURCE_DIR"] = TMP

from backend.app.database import DB_PATH, get_connection, init_db  # noqa: E402


def ms(samples):
    return {
        "n": len(samples),
        "p50_ms": round(statistics.median(samples) * 1000, 3),
        "p95_ms": round(sorted(samples)[max(0, int(len(samples) * 0.95) - 1)] * 1000, 3),
    }


def build_synthetic():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    words_json = "[" + ",".join(['{"w":"word","t":0.1}'] * 8) + "]"
    conn.execute("BEGIN")
    for i in range(43):
        exam_id = f"y{2000 + i}-06-set1"
        conn.execute(
            "INSERT INTO exams (id, year, month, set_number, title, audio_file, audio_duration, is_golden) VALUES (?,?,?,?,?,?,?,0)",
            (exam_id, 2000 + i, 6, 1, exam_id, f"{exam_id}.mp3", 1500),
        )
        for s in range(7):
            section_id = f"{exam_id}-sec-{s}"
            subpart_id = f"{exam_id}-sp-{s}"
            conn.execute(
                "INSERT INTO sections (id, exam_id, type, title, order_num) VALUES (?,?,?,?,?)",
                (section_id, exam_id, "conversation", section_id, s),
            )
            conn.execute(
                """
                INSERT INTO subparts
                    (id, section_id, exam_id, type, title, order_num, start_time, end_time, questions_json)
                VALUES (?,?,?,?,?,?,?,?, '[]')
                """,
                (subpart_id, section_id, exam_id, "conversation", subpart_id, s, 0, 60),
            )
            for n in range(22):
                conn.execute(
                    """
                    INSERT INTO sentences
                        (id, exam_id, section_id, subpart_id, order_num, speaker, start_time, end_time, english, chinese, words_json, confidence)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,1)
                    """,
                    (
                        f"{subpart_id}-{n}",
                        exam_id,
                        section_id,
                        subpart_id,
                        n,
                        "M",
                        n,
                        n + 0.8,
                        "synthetic sentence",
                        "合成句",
                        words_json,
                    ),
                )
    for i in range(20000):
        conn.execute(
            "INSERT INTO vocab_frequency (word, frequency, exam_count, phonetic, definition_zh, examples_json) VALUES (?,?,?,?,?, '[]')",
            (f"w{i}", 20000 - i, 1, "w", "义"),
        )
    now = time.time()
    for i in range(200):
        word = f"w{i}" if i < 170 else f"missing{i}"
        conn.execute(
            """
            INSERT INTO user_vocab_srs
                (user_id, word, state, stability, difficulty, reps, lapses, due, updated_at)
            VALUES ('gst_bench', ?, 'review', 1, 5, 2, 0, ?, ?)
            """,
            (word, now - 60, now),
        )
    conn.commit()
    conn.close()


def time_call(fn, rounds=30):
    samples = []
    for _ in range(rounds):
        start = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - start)
    return ms(samples)


def main():
    assert Path(DB_PATH).resolve().is_relative_to(Path(TMP).resolve())
    build_synthetic()
    conn = sqlite3.connect(DB_PATH)
    sentence_count = conn.execute("SELECT COUNT(*) FROM sentences").fetchone()[0]
    sentence_bytes = conn.execute("SELECT SUM(LENGTH(words_json)) FROM sentences").fetchone()[0]
    conn.close()

    def list_exams():
        c = get_connection()
        c.execute("SELECT id, year, month, set_number, title FROM exams ORDER BY year DESC").fetchall()
        c.close()

    def one_subpart_sentences():
        c = get_connection()
        c.execute(
            "SELECT id, english, chinese, words_json FROM sentences WHERE exam_id = ? AND subpart_id = ? ORDER BY order_num",
            ("y2020-06-set1", "y2020-06-set1-sp-0"),
        ).fetchall()
        c.close()

    def due_inner():
        c = get_connection()
        c.execute(
            """
            SELECT uvs.word FROM user_vocab_srs uvs
            JOIN vocab_frequency vf ON uvs.word = vf.word
            WHERE uvs.user_id = 'gst_bench' AND uvs.due <= ? AND uvs.state = 'review'
            """,
            (time.time(),),
        ).fetchall()
        c.close()

    def due_left():
        c = get_connection()
        rows = c.execute(
            """
            SELECT uvs.word, vf.word FROM user_vocab_srs uvs
            LEFT JOIN vocab_frequency vf ON uvs.word = vf.word
            WHERE uvs.user_id = 'gst_bench' AND uvs.due <= ? AND uvs.state = 'review'
            """,
            (time.time(),),
        ).fetchall()
        c.close()
        return rows

    left_rows = due_left()
    inner_count = len(sqlite3.connect(DB_PATH).execute(
        """
        SELECT uvs.word FROM user_vocab_srs uvs
        JOIN vocab_frequency vf ON uvs.word = vf.word
        WHERE uvs.user_id = 'gst_bench' AND uvs.state = 'review'
        """
    ).fetchall())

    def simulated(delay, parallel_first, extra_serial):
        start = time.perf_counter()
        if parallel_first:
            time.sleep(delay)
        else:
            time.sleep(delay)
        for _ in range(extra_serial):
            time.sleep(delay)
        return time.perf_counter() - start

    delay = 0.08
    before = [simulated(delay, True, 1) for _ in range(5)]
    after = [simulated(delay, True, 0) for _ in range(5)]

    print("ISOLATED_BENCH")
    print(f"db={DB_PATH}")
    print(f"synthetic_sentences={sentence_count} words_json_bytes={sentence_bytes}")
    print(f"list_exams {time_call(list_exams)}")
    print(f"subpart_sentences {time_call(one_subpart_sentences)}")
    print(f"due_inner_join {time_call(due_inner)} rows_kept={inner_count}")
    print(f"due_left_join {time_call(due_left)} rows_kept={len(left_rows)}")
    print(
        "homepage_rtt_model_before_serial_subparts_s",
        round(statistics.median(before), 3),
        "after_parallel_hint_s",
        round(statistics.median(after), 3),
        "injected_rtt_s",
        delay,
    )
    print("NOTE not production latency; no network to 43.142.98.29")


if __name__ == "__main__":
    main()
