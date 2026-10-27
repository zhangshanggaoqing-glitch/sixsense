import json
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from backend.app.config import DATA_DIR
from backend.app.database import get_connection

router = APIRouter(prefix="/api/full-papers", tags=["FullPapers"])

MANIFEST_PATH = DATA_DIR / "full_paper_manifest.json"

def load_manifest() -> List[dict]:
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading full_paper_manifest: {e}")
    return []

@router.get("")
def list_full_papers(all: bool = Query(False)):
    """
    List full papers from full_paper_manifest.json.
    Default returns only published: true.
    """
    items = load_manifest()
    if not items:
        # Fallback to query exams if manifest is missing
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT id, year, month, set_number, title, audio_file, audio_duration
            FROM exams
            ORDER BY year DESC, month DESC, set_number ASC
        """)
        rows = c.fetchall()
        conn.close()
        for r in rows:
            items.append({
                "id": r["id"],
                "year": r["year"],
                "month": r["month"],
                "set": r["set_number"],
                "title_zh": f"{r['year']}年{r['month']}月 六级 第{r['set_number']}套 · 完整听力",
                "audio_file": r["audio_file"],
                "audio_src": f"/api/audio/{r['audio_file']}",
                "download_url": f"/api/audio/{r['audio_file']}?download=1",
                "audio_bytes": 0,
                "duration_sec": r["audio_duration"],
                "question_count": 25,
                "published": True
            })

    if not all:
        return [p for p in items if p.get("published")]
    return items

@router.get("/{paper_id}")
def get_full_paper_detail(paper_id: str):
    """
    Get full paper metadata and all 25 questions grouped by Section & Subpart.
    """
    manifest = load_manifest()
    paper_meta = next((p for p in manifest if p["id"] == paper_id), None)

    conn = get_connection()
    c = conn.cursor()

    if not paper_meta:
        c.execute("SELECT id, year, month, set_number, title, audio_file, audio_duration FROM exams WHERE id = ?", (paper_id,))
        exam_row = c.fetchone()
        if not exam_row:
            conn.close()
            raise HTTPException(status_code=404, detail="Full paper not found")
        paper_meta = {
            "id": exam_row["id"],
            "year": exam_row["year"],
            "month": exam_row["month"],
            "set": exam_row["set_number"],
            "title_zh": f"{exam_row['year']}年{exam_row['month']}月 六级 第{exam_row['set_number']}套 · 完整听力",
            "audio_file": exam_row["audio_file"],
            "audio_src": f"/api/audio/{exam_row['audio_file']}",
            "download_url": f"/api/audio/{exam_row['audio_file']}?download=1",
            "audio_bytes": 0,
            "duration_sec": exam_row["audio_duration"],
            "question_count": 25,
            "published": True
        }

    # Fetch sections
    c.execute("SELECT id, type, title, order_num FROM sections WHERE exam_id = ? ORDER BY order_num ASC", (paper_id,))
    section_rows = c.fetchall()

    # Fetch all subparts
    c.execute("""
        SELECT id, section_id, type, title, topic_zh, question_range, order_num
        FROM subparts
        WHERE exam_id = ?
        ORDER BY order_num ASC
    """, (paper_id,))
    subpart_rows = c.fetchall()

    # Fetch all questions
    c.execute("""
        SELECT id, exam_id, subpart_id, question_num, prompt, option_a, option_b, option_c, option_d, correct_answer, explanation
        FROM questions
        WHERE exam_id = ?
        ORDER BY question_num ASC
    """, (paper_id,))
    question_rows = c.fetchall()
    conn.close()

    # Organize questions into subparts, then sections
    questions_by_subpart = {}
    for q in question_rows:
        sp_id = q["subpart_id"]
        if sp_id not in questions_by_subpart:
            questions_by_subpart[sp_id] = []
        questions_by_subpart[sp_id].append({
            "id": q["id"],
            "question_num": q["question_num"],
            "prompt": q["prompt"],
            "options": {
                "A": q["option_a"],
                "B": q["option_b"],
                "C": q["option_c"],
                "D": q["option_d"],
            },
            "correct_answer": q["correct_answer"],
            "explanation": q["explanation"],
        })

    subparts_by_section = {}
    for sp in subpart_rows:
        sec_id = sp["section_id"]
        if sec_id not in subparts_by_section:
            subparts_by_section[sec_id] = []
        subparts_by_section[sec_id].append({
            "id": sp["id"],
            "title": sp["title"],
            "topic_zh": sp["topic_zh"],
            "question_range": sp["question_range"],
            "questions": questions_by_subpart.get(sp["id"], [])
        })

    sections = []
    for sec in section_rows:
        sec_id = sec["id"]
        sections.append({
            "id": sec_id,
            "title": sec["title"],
            "subparts": subparts_by_section.get(sec_id, [])
        })

    result = dict(paper_meta)
    result["sections"] = sections
    return result
