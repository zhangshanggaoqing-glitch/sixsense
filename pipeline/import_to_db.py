import json
import sqlite3
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ALIGNMENT_FILE = BASE_DIR / "data" / "derived" / "exams" / "2020-07-set1" / "alignment.json"
DB_PATH = BASE_DIR / "data" / "sixsense.db"

def import_to_db():
    if not ALIGNMENT_FILE.exists():
        print(f"Alignment file {ALIGNMENT_FILE} does not exist yet.")
        return

    with open(ALIGNMENT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    exam_id = data["exam_id"]
    cursor.execute("""
        INSERT INTO exams (id, year, month, set_number, title, audio_file, audio_duration, is_golden)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            audio_file = excluded.audio_file,
            audio_duration = excluded.audio_duration,
            is_golden = 1;
    """, (
        exam_id, 2020, 7, 1, data["title"], data["audio_file"], data["audio_duration"]
    ))

    # Clear old data for this exam
    cursor.execute("DELETE FROM sentences WHERE exam_id = ?", (exam_id,))
    cursor.execute("DELETE FROM subparts WHERE exam_id = ?", (exam_id,))
    cursor.execute("DELETE FROM sections WHERE exam_id = ?", (exam_id,))

    # Map sections
    section_map = {
        "Section A": {"id": f"{exam_id}-sec-a", "title": "Section A: Long Conversations", "order": 1},
        "Section B": {"id": f"{exam_id}-sec-b", "title": "Section B: Listening Passages", "order": 2},
        "Section C": {"id": f"{exam_id}-sec-c", "title": "Section C: Recorded Lectures/Talks", "order": 3}
    }

    for s_name, s_info in section_map.items():
        cursor.execute("""
            INSERT INTO sections (id, exam_id, type, title, order_num)
            VALUES (?, ?, ?, ?, ?);
        """, (s_info["id"], exam_id, s_name, s_info["title"], s_info["order"]))

    subpart_order = 1
    total_sentences_inserted = 0

    for sp in data["subparts"]:
        sec_name = sp["section"]
        sec_id = section_map[sec_name]["id"]
        sp_id = f"{exam_id}-{sp['subpart_id']}"

        cursor.execute("""
            INSERT INTO subparts (id, section_id, exam_id, type, title, order_num, start_time, end_time, questions_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '[]');
        """, (
            sp_id, sec_id, exam_id, sp.get("type", "conversation"),
            sp["title"], subpart_order, sp["start_time"], sp["end_time"]
        ))
        subpart_order += 1

        for s in sp["sentences"]:
            cursor.execute("""
                INSERT INTO sentences (
                    id, exam_id, section_id, subpart_id, order_num,
                    speaker, start_time, end_time, english, chinese, confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                s["id"], exam_id, sec_id, sp_id, s["order"],
                s.get("speaker", ""), s["start_time"], s["end_time"],
                s["english"], s["chinese"], s.get("confidence", 0.95)
            ))
            total_sentences_inserted += 1

    # Set default resume state
    cursor.execute("""
        INSERT INTO user_state (key, value_json, updated_at)
        VALUES ('last_resume', ?, ?)
        ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = excluded.updated_at;
    """, (
        json.dumps({
            "exam_id": exam_id,
            "section_id": section_map["Section A"]["id"],
            "subpart_id": f"{exam_id}-conv-1",
            "sentence_index": 0,
            "playback_rate": 1.0,
            "display_mode": "C",
            "loop_mode": "off",
            "volume": 1.0
        }, ensure_ascii=False),
        time.time()
    ))

    conn.commit()
    conn.close()
    print(f"Imported exam {exam_id}: {len(data['subparts'])} subparts, {total_sentences_inserted} sentences.")

if __name__ == "__main__":
    import_to_db()
