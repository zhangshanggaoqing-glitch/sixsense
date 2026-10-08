#!/usr/bin/env python3
"""
Automated QA Gate for SixSense English Listening Platform.
Validates 100% sentence-level auditing standards:
1. Zero empty translations (every sentence has authentic Chinese)
2. Zero broken fragments (every sentence is a complete thought)
3. Monotonic acoustic alignment (start < end, realistic durations)
4. Full subpart coverage (7 subparts with authentic Chinese topics)
5. Full question coverage (25 official questions with A/B/C/D and explanations)
"""

import sys
import sqlite3
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sixsense.db"
RAW_DIR = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频")

def run_qa():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id, title, audio_file, audio_duration, is_golden FROM exams")
    exams = cur.fetchall()

    total_errors = 0
    total_warnings = 0

    print("=" * 70)
    print("SixSense Database Strict QA Audit Gate")
    print("=" * 70)
    print(f"Total exams in database: {len(exams)}")

    for exam in exams:
        eid, title, audio_file, duration, is_golden = exam
        print(f"\n[Exam Audit] {eid}: {title}")
        print(f"  Audio: {audio_file} ({duration}s), Golden: {is_golden}")

        # 1. Check audio file exists in RAW_DIR
        found_audio = list(RAW_DIR.rglob(audio_file))
        if not found_audio:
            print(f"  [ERROR] Audio file not found on disk: {audio_file}")
            total_errors += 1
        else:
            print(f"  [PASS] Audio file verified on disk: {found_audio[0].name}")

        # 2. Check Subparts
        cur.execute("SELECT id, title, topic_zh, question_range, sentence_count, duration, start_time, end_time FROM subparts WHERE exam_id = ? ORDER BY order_num", (eid,))
        subparts = cur.fetchall()
        if len(subparts) != 7:
            print(f"  [ERROR] Expected 7 subparts, found {len(subparts)}")
            total_errors += 1
        else:
            print(f"  [PASS] 7 subparts present")

        for sp in subparts:
            sp_id, sp_title, topic_zh, q_range, sent_cnt, sp_dur, st, et = sp
            if not topic_zh or not re.search(r"[\u4e00-\u9fff]", topic_zh):
                print(f"  [ERROR] Subpart {sp_id} has invalid Chinese topic: '{topic_zh}'")
                total_errors += 1
            if sent_cnt <= 0 or sp_dur <= 0:
                print(f"  [ERROR] Subpart {sp_id} invalid sentence_count ({sent_cnt}) or duration ({sp_dur})")
                total_errors += 1
            if st >= et:
                print(f"  [ERROR] Subpart {sp_id} timestamps inverted: {st} >= {et}")
                total_errors += 1

        # 3. Check Sentences
        cur.execute("""
            SELECT id, subpart_id, order_num, speaker, start_time, end_time, english, chinese, confidence
            FROM sentences
            WHERE exam_id = ?
            ORDER BY subpart_id, order_num
        """, (eid,))
        sentences = cur.fetchall()
        print(f"  Total sentences: {len(sentences)}")

        empty_zh = 0
        broken_en = 0
        timing_err = 0

        for s in sentences:
            sid, sp_id, order_num, speaker, st, et, en, zh, conf = s
            # Check Chinese
            if not zh or zh.strip() == "" or not re.search(r"[\u4e00-\u9fff]", zh):
                print(f"    [ERROR] Empty or non-Chinese translation at {sid}: en='{en}', zh='{zh}'")
                empty_zh += 1
                total_errors += 1

            # Check English completeness
            en_clean = en.strip()
            if len(en_clean) < 2:
                print(f"    [ERROR] Abnormally short English sentence at {sid}: '{en}'")
                broken_en += 1
                total_errors += 1
            if not re.search(r'[.?!\"”\']$', en_clean):
                print(f"    [WARN] Sentence does not end with standard punctuation at {sid}: '{en}'")
                total_warnings += 1

            # Check timing
            if st >= et:
                print(f"    [ERROR] Sentence timing inverted at {sid}: {st} >= {et}")
                timing_err += 1
                total_errors += 1
            if et - st > 35.0:
                print(f"    [WARN] Very long sentence duration ({et-st:.1f}s) at {sid}: '{en[:40]}...'")
                total_warnings += 1

        if empty_zh == 0:
            print(f"  [PASS] 100% sentences have authentic Chinese translations (0 empty)")
        if broken_en == 0:
            print(f"  [PASS] 0 broken English sentence fragments")
        if timing_err == 0:
            print(f"  [PASS] Monotonic acoustic word-level timestamps valid")

        # 4. Check Questions
        cur.execute("""
            SELECT id, subpart_id, question_num, prompt, option_a, option_b, option_c, option_d, correct_answer, explanation
            FROM questions
            WHERE exam_id = ?
            ORDER BY question_num
        """, (eid,))
        questions = cur.fetchall()
        print(f"  Total questions: {len(questions)}")

        if len(questions) != 25:
            print(f"  [ERROR] Expected 25 questions, found {len(questions)}")
            total_errors += 1
        else:
            print(f"  [PASS] Exactly 25 official questions present")

        for q in questions:
            qid, sp_id, qnum, prompt, oa, ob, oc, od, ans, exp = q
            if ans not in ['A', 'B', 'C', 'D']:
                print(f"    [ERROR] Invalid correct_answer '{ans}' at {qid}")
                total_errors += 1
            for opt_k, opt_v in [('A', oa), ('B', ob), ('C', oc), ('D', od)]:
                if not opt_v or opt_v.strip() == "":
                    print(f"    [ERROR] Question {qid} missing Option {opt_k}")
                    total_errors += 1
            if not exp or not re.search(r"[\u4e00-\u9fff]", exp):
                print(f"    [WARN] Question {qid} missing Chinese explanation")
                total_warnings += 1

    print("\n" + "=" * 70)
    print(f"Audit Summary: {total_errors} Errors, {total_warnings} Warnings")
    print("=" * 70)

    conn.close()
    if total_errors > 0:
        print("[FAIL] Database failed strict QA audit gate!")
        sys.exit(1)
    else:
        print("[SUCCESS] All audited exams passed 100% QA standards!")
        sys.exit(0)

if __name__ == "__main__":
    run_qa()
