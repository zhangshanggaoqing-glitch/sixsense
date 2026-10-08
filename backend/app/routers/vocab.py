import time
import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.database import get_connection

router = APIRouter(prefix="/api/vocab", tags=["Vocabulary"])

class AddVocabRequest(BaseModel):
    word: str
    lemma: Optional[str] = None
    phonetic: Optional[str] = ""
    part_of_speech: Optional[str] = ""
    definition_zh: Optional[str] = ""
    cet_level: Optional[str] = "CET-6"
    source_sentence_id: Optional[str] = ""
    source_sentence_en: Optional[str] = ""
    source_sentence_zh: Optional[str] = ""
    exam_id: Optional[str] = ""
    audio_clip_start: Optional[float] = 0.0
    audio_clip_end: Optional[float] = 0.0

@router.get("")
def list_vocabulary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM vocabulary
        ORDER BY created_at DESC;
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.post("")
def add_vocabulary(req: AddVocabRequest):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if word in same sentence already added
    cursor.execute("SELECT id FROM vocabulary WHERE word = ? AND source_sentence_id = ?", (req.word.lower(), req.source_sentence_id))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return {"id": existing["id"], "status": "already_exists"}

    item_id = f"vocab_{uuid.uuid4().hex[:10]}"
    now = time.time()
    lemma = req.lemma or req.word.lower()

    cursor.execute("""
        INSERT INTO vocabulary (
            id, word, lemma, phonetic, part_of_speech, definition_zh, cet_level,
            source_sentence_id, source_sentence_en, source_sentence_zh, exam_id,
            audio_clip_start, audio_clip_end, created_at, review_count, mastery
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0.0);
    """, (
        item_id, req.word.lower(), lemma, req.phonetic, req.part_of_speech, req.definition_zh, req.cet_level,
        req.source_sentence_id, req.source_sentence_en, req.source_sentence_zh, req.exam_id,
        req.audio_clip_start, req.audio_clip_end, now
    ))
    conn.commit()
    conn.close()
    return {"id": item_id, "status": "added"}

@router.delete("/{vocab_id}")
def delete_vocabulary(vocab_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vocabulary WHERE id = ?", (vocab_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}
