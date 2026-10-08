import json
from fastapi import APIRouter, HTTPException, Query
from backend.app.database import get_connection

router = APIRouter(prefix="/api/exams", tags=["Exams"])

@router.get("")
def list_exams():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, year, month, set_number, title, audio_file, audio_duration, is_golden
        FROM exams
        ORDER BY year DESC, month DESC, set_number ASC;
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/{exam_id}")
def get_exam_detail(exam_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exams WHERE id = ?", (exam_id,))
    exam = cursor.fetchone()
    if not exam:
        conn.close()
        raise HTTPException(status_code=404, detail="Exam not found")

    cursor.execute("SELECT * FROM sections WHERE exam_id = ? ORDER BY order_num ASC", (exam_id,))
    sections = [dict(s) for s in cursor.fetchall()]

    for sec in sections:
        cursor.execute("SELECT * FROM subparts WHERE section_id = ? ORDER BY order_num ASC", (sec["id"],))
        subparts = [dict(sp) for sp in cursor.fetchall()]
        for sp in subparts:
            sp["questions"] = json.loads(sp.get("questions_json") or "[]")
        sec["subparts"] = subparts

    conn.close()
    exam_dict = dict(exam)
    exam_dict["sections"] = sections
    return exam_dict

@router.get("/{exam_id}/subparts")
def get_subparts(exam_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sp.id, sp.exam_id, sp.section_id, sec.title as section_title, sp.type, sp.title,
               sp.topic_zh, sp.question_range, sp.order_num, sp.start_time, sp.end_time,
               sp.sentence_count, sp.duration
        FROM subparts sp
        JOIN sections sec ON sp.section_id = sec.id
        WHERE sp.exam_id = ?
        ORDER BY sp.order_num ASC;
    """, (exam_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/{exam_id}/subparts/{subpart_id}/questions")
def get_subpart_questions(exam_id: str, subpart_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, exam_id, subpart_id, question_num, prompt, option_a, option_b, option_c, option_d, correct_answer, explanation
        FROM questions
        WHERE exam_id = ? AND subpart_id = ?
        ORDER BY question_num ASC;
    """, (exam_id, subpart_id))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/{exam_id}/sentences")
def get_sentences(exam_id: str, subpart_id: str = Query(None)):
    conn = get_connection()
    cursor = conn.cursor()
    if subpart_id:
        cursor.execute("""
            SELECT id, exam_id, section_id, subpart_id, order_num, speaker, start_time, end_time, english, chinese, words_json, confidence
            FROM sentences
            WHERE exam_id = ? AND subpart_id = ?
            ORDER BY order_num ASC;
        """, (exam_id, subpart_id))
    else:
        cursor.execute("""
            SELECT id, exam_id, section_id, subpart_id, order_num, speaker, start_time, end_time, english, chinese, words_json, confidence
            FROM sentences
            WHERE exam_id = ?
            ORDER BY order_num ASC;
        """, (exam_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

