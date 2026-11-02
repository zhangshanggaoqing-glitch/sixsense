import time
import uuid
import json
import re
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from backend.app.database import get_connection
from backend.app.utils.auth import get_current_user_optional
from backend.app.routers.dict import query_youdao
from backend.app.utils import fsrs

router = APIRouter(prefix="/api/vocab", tags=["Vocabulary"])

# ==============================================================================
# Pydantic Request Models
# ==============================================================================

class AddVocabRequest(BaseModel):
    word: str
    lemma: Optional[str] = None
    phonetic: Optional[str] = ""
    phonetic_uk: Optional[str] = ""
    phonetic_us: Optional[str] = ""
    audio_uk: Optional[str] = ""
    audio_us: Optional[str] = ""
    part_of_speech: Optional[str] = ""
    definition_zh: Optional[str] = ""
    cet_level: Optional[str] = "CET-6"
    source_sentence_id: Optional[str] = ""
    source_sentence_en: Optional[str] = ""
    source_sentence_zh: Optional[str] = ""
    exam_id: Optional[str] = ""
    audio_clip_start: Optional[float] = 0.0
    audio_clip_end: Optional[float] = 0.0

class UpdateStatusRequest(BaseModel):
    word: str
    status: str  # 'known' | 'learning'

class SyncStatusItem(BaseModel):
    word: str
    status: str
    updated_at: Optional[float] = None

class SyncStatusRequest(BaseModel):
    items: List[SyncStatusItem]

class VocabSettingsRequest(BaseModel):
    daily_new_quota: Optional[int] = Field(20, ge=1, le=100)
    autoplay_audio: Optional[bool] = True

class RateCardRequest(BaseModel):
    word: str
    rating: int  # 1: Again (不会), 2: Hard (模糊), 3: Good (会了+测验通过)
    quiz_passed: Optional[bool] = None
    listen_count: Optional[int] = 1

class TelemetryEventRequest(BaseModel):
    event_name: str
    word: Optional[str] = ""
    payload: Optional[Dict[str, Any]] = None

def clean_definition(pos: str, meaning: str) -> str:
    """Keep concise 1-line definition (avoid clutter)."""
    if not meaning:
        return ""
    parts = [p.strip() for p in re.split(r"[；;]", meaning) if p.strip()]
    concise = "；".join(parts[:2]) if parts else meaning
    return f"{pos} {concise}".strip() if pos else concise

def get_today_start_ts() -> float:
    """Returns unix timestamp for 00:00:00 of today in local/UTC date."""
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day, 0, 0, 0)
    return midnight.timestamp()

# ==============================================================================
# Legacy / Studio Bookmark Endpoints
# ==============================================================================

@router.get("")
def list_vocabulary(current_user: dict = Depends(get_current_user_optional)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM vocabulary
        WHERE user_id = ?
        ORDER BY created_at DESC;
    """, (current_user["id"],))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.post("")
def add_vocabulary(req: AddVocabRequest, current_user: dict = Depends(get_current_user_optional)):
    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]
    
    cursor.execute(
        "SELECT id FROM vocabulary WHERE word = ? AND source_sentence_id = ? AND user_id = ?",
        (req.word.lower(), req.source_sentence_id, user_id)
    )
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return {"id": existing["id"], "status": "already_exists"}

    item_id = f"vocab_{uuid.uuid4().hex[:10]}"
    now = time.time()
    lemma = req.lemma or req.word.lower()

    cursor.execute("""
        INSERT INTO vocabulary (
            id, word, lemma, phonetic, phonetic_uk, phonetic_us, audio_uk, audio_us,
            part_of_speech, definition_zh, cet_level,
            source_sentence_id, source_sentence_en, source_sentence_zh, exam_id,
            audio_clip_start, audio_clip_end, created_at, review_count, mastery, user_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0.0, ?);
    """, (
        item_id, req.word.lower(), lemma, req.phonetic, req.phonetic_uk, req.phonetic_us, req.audio_uk, req.audio_us,
        req.part_of_speech, req.definition_zh, req.cet_level,
        req.source_sentence_id, req.source_sentence_en, req.source_sentence_zh, req.exam_id,
        req.audio_clip_start, req.audio_clip_end, now, user_id
    ))
    conn.commit()
    conn.close()
    return {"id": item_id, "status": "added"}

# ==============================================================================
# Phase 1: CET-6 Listening Frequency Endpoints
# ==============================================================================

@router.get("/freq")
def list_freq_vocabulary(
    tab: str = Query("unmastered", pattern="^(unmastered|mastered|all)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    q: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user_optional)
):
    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]

    cursor.execute("""
        SELECT COUNT(*) FROM user_vocab_status
        WHERE user_id = ? AND status = 'known'
    """, (user_id,))
    mastered_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vocab_frequency;")
    total_corpus_words = cursor.fetchone()[0]
    remaining_count = max(0, total_corpus_words - mastered_count)

    where_clauses = []
    params = []

    if tab == "unmastered":
        where_clauses.append("(uvs.status IS NULL OR uvs.status != 'known')")
    elif tab == "mastered":
        where_clauses.append("uvs.status = 'known'")

    if q and q.strip():
        search_term = f"%{q.strip().lower()}%"
        where_clauses.append("(vf.word LIKE ? OR vf.definition_zh LIKE ?)")
        params.extend([search_term, search_term])

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    count_sql = f"""
        SELECT COUNT(*)
        FROM vocab_frequency vf
        LEFT JOIN user_vocab_status uvs ON vf.word = uvs.word AND uvs.user_id = ?
        {where_sql}
    """
    cursor.execute(count_sql, [user_id] + params)
    tab_total = cursor.fetchone()[0]

    offset = (page - 1) * limit
    data_sql = f"""
        SELECT
            vf.word, vf.frequency, vf.exam_count,
            vf.phonetic, vf.phonetic_uk, vf.phonetic_us,
            vf.pos, vf.definition_zh, vf.tags_json, vf.examples_json,
            COALESCE(uvs.status, 'new') AS status
        FROM vocab_frequency vf
        LEFT JOIN user_vocab_status uvs ON vf.word = uvs.word AND uvs.user_id = ?
        {where_sql}
        ORDER BY vf.frequency DESC, vf.exam_count DESC
        LIMIT ? OFFSET ?;
    """
    cursor.execute(data_sql, [user_id] + params + [limit, offset])
    rows = cursor.fetchall()

    items = []
    for r in rows:
        d = dict(r)
        examples = json.loads(d.pop("examples_json", "[]") or "[]")
        tags = json.loads(d.pop("tags_json", "[]") or "[]")
        d["example_count"] = len(examples)
        d["tags"] = tags
        items.append(d)

    conn.close()
    return {
        "items": items,
        "total_count": tab_total,
        "mastered_count": mastered_count,
        "remaining_count": remaining_count,
        "page": page,
        "limit": limit,
        "has_more": offset + len(items) < tab_total
    }

@router.get("/freq/{word}")
def get_freq_word_detail(word: str, current_user: dict = Depends(get_current_user_optional)):
    clean_w = word.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]

    cursor.execute("""
        SELECT
            vf.word, vf.frequency, vf.exam_count,
            vf.phonetic, vf.phonetic_uk, vf.phonetic_us,
            vf.pos, vf.definition_zh, vf.tags_json, vf.examples_json,
            COALESCE(uvs.status, 'new') AS status
        FROM vocab_frequency vf
        LEFT JOIN user_vocab_status uvs ON vf.word = uvs.word AND uvs.user_id = ?
        WHERE vf.word = ?;
    """, (user_id, clean_w))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Word not found in frequency database")

    d = dict(row)
    examples = json.loads(d.pop("examples_json", "[]") or "[]")
    tags = json.loads(d.pop("tags_json", "[]") or "[]")
    d["examples"] = examples
    d["tags"] = tags

    # Fetch distractors
    cursor.execute("SELECT distractors_json FROM vocab_distractors WHERE word = ?;", (clean_w,))
    dist_row = cursor.fetchone()
    d["distractors"] = json.loads(dist_row[0]) if dist_row else []

    conn.close()
    return d

@router.post("/freq/status")
def update_freq_status(req: UpdateStatusRequest, current_user: dict = Depends(get_current_user_optional)):
    if req.status not in ("known", "learning", "new"):
        raise HTTPException(status_code=400, detail="Invalid status")

    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]
    now = time.time()
    clean_w = req.word.strip().lower()

    cursor.execute("""
        INSERT INTO user_vocab_status (user_id, word, status, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, word) DO UPDATE SET
            status = excluded.status,
            updated_at = excluded.updated_at;
    """, (user_id, clean_w, req.status, now))
    conn.commit()
    conn.close()
    return {"status": "ok", "word": clean_w, "new_status": req.status}

@router.post("/freq/sync")
def sync_freq_status(req: SyncStatusRequest, current_user: dict = Depends(get_current_user_optional)):
    if not req.items:
        return {"status": "ok", "synced_count": 0}

    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]
    now = time.time()

    data = [
        (user_id, it.word.strip().lower(), it.status, it.updated_at or now)
        for it in req.items if it.status in ("known", "learning")
    ]

    cursor.executemany("""
        INSERT INTO user_vocab_status (user_id, word, status, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, word) DO UPDATE SET
            status = excluded.status,
            updated_at = excluded.updated_at;
    """, data)
    conn.commit()
    conn.close()
    return {"status": "ok", "synced_count": len(data)}

# ==============================================================================
# Phase 2: SRS Memory Curve, Daily Quota, & Discrimination Session
# ==============================================================================

@router.get("/settings")
def get_user_vocab_settings(current_user: dict = Depends(get_current_user_optional)):
    """Get user's daily quota and playback preferences."""
    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]

    cursor.execute("""
        SELECT daily_new_quota, autoplay_audio, algorithm_version
        FROM user_vocab_settings WHERE user_id = ?;
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "daily_new_quota": row[0],
            "autoplay_audio": bool(row[1]),
            "algorithm_version": row[2]
        }
    return {
        "daily_new_quota": 20,
        "autoplay_audio": True,
        "algorithm_version": "FSRS-5.0.0"
    }

@router.post("/settings")
def save_user_vocab_settings(req: VocabSettingsRequest, current_user: dict = Depends(get_current_user_optional)):
    """Update user's daily new words quota and playback preferences."""
    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]
    now = time.time()

    quota = min(100, max(1, req.daily_new_quota or 20))
    autoplay = 1 if req.autoplay_audio else 0

    cursor.execute("""
        INSERT INTO user_vocab_settings (user_id, daily_new_quota, autoplay_audio, algorithm_version, updated_at)
        VALUES (?, ?, ?, 'FSRS-5.0.0', ?)
        ON CONFLICT(user_id) DO UPDATE SET
            daily_new_quota = excluded.daily_new_quota,
            autoplay_audio = excluded.autoplay_audio,
            updated_at = excluded.updated_at;
    """, (user_id, quota, autoplay, now))
    conn.commit()
    conn.close()
    return {"status": "ok", "daily_new_quota": quota, "autoplay_audio": bool(autoplay)}

@router.get("/summary")
def get_daily_srs_summary(current_user: dict = Depends(get_current_user_optional)):
    """
    Returns concise daily numbers:
    新词 a/A · 复习 b · 到期 c
    """
    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]
    now = time.time()
    today_start = get_today_start_ts()

    # 1. User settings
    cursor.execute("SELECT daily_new_quota FROM user_vocab_settings WHERE user_id = ?;", (user_id,))
    q_row = cursor.fetchone()
    quota_A = q_row[0] if q_row else 20

    # 2. New words learned today (a): first review today
    cursor.execute("""
        SELECT COUNT(*) FROM user_vocab_srs
        WHERE user_id = ? AND reps = 1 AND last_review >= ?;
    """, (user_id, today_start))
    new_a = cursor.fetchone()[0]

    # 3. Total active cards in review pool (b)
    cursor.execute("""
        SELECT COUNT(*) FROM user_vocab_srs
        WHERE user_id = ? AND state IN ('learning', 'review', 'relearning');
    """, (user_id,))
    review_b = cursor.fetchone()[0]

    # 4. Due review cards waiting right now (c): due <= now
    cursor.execute("""
        SELECT COUNT(*) FROM user_vocab_srs
        WHERE user_id = ? AND due <= ? AND state IN ('learning', 'review', 'relearning');
    """, (user_id, now))
    due_c = cursor.fetchone()[0]

    # 5. Total mastered (reps >= 2 and state == 'review')
    cursor.execute("""
        SELECT COUNT(*) FROM user_vocab_srs
        WHERE user_id = ? AND state = 'review' AND reps >= 2;
    """, (user_id,))
    mastered_count = cursor.fetchone()[0]

    conn.close()

    summary_text = f"新词 {new_a}/{quota_A} · 复习 {review_b} · 到期 {due_c}"

    return {
        "new_today": new_a,
        "new_quota": quota_A,
        "review_total": review_b,
        "due_count": due_c,
        "mastered_count": mastered_count,
        "summary_text": summary_text
    }

@router.get("/session")
def get_study_session(current_user: dict = Depends(get_current_user_optional)):
    """
    Builds the daily study queue according to core priority:
    1. Due review cards first (due <= now, ordered by due ASC, stability ASC)
    2. Then new cards up to daily quota (max(0, quota - new_today))
    """
    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]
    now = time.time()
    today_start = get_today_start_ts()

    # User quota
    cursor.execute("SELECT daily_new_quota FROM user_vocab_settings WHERE user_id = ?;", (user_id,))
    q_row = cursor.fetchone()
    daily_quota = q_row[0] if q_row else 20

    # New words learned today
    cursor.execute("""
        SELECT COUNT(*) FROM user_vocab_srs
        WHERE user_id = ? AND reps = 1 AND last_review >= ?;
    """, (user_id, today_start))
    new_learned_today = cursor.fetchone()[0]
    remaining_new_quota = max(0, daily_quota - new_learned_today)

    session_items = []
    seen_words = set()

    # Priority 1: Due Review Cards (due <= now)
    cursor.execute("""
        SELECT
            uvs.word, uvs.state, uvs.stability, uvs.difficulty, uvs.reps, uvs.lapses, uvs.due,
            vf.frequency, vf.exam_count, vf.phonetic, vf.pos, vf.definition_zh, vf.examples_json,
            vd.distractors_json
        FROM user_vocab_srs uvs
        JOIN vocab_frequency vf ON uvs.word = vf.word
        LEFT JOIN vocab_distractors vd ON uvs.word = vd.word
        WHERE uvs.user_id = ? AND uvs.due <= ? AND uvs.state IN ('learning', 'review', 'relearning')
        ORDER BY uvs.due ASC, uvs.stability ASC
        LIMIT 60;
    """, (user_id, now))
    due_rows = cursor.fetchall()

    for r in due_rows:
        w = r[0]
        seen_words.add(w)
        examples = json.loads(r[12] or "[]")
        distractors = json.loads(r[13] or "[]")
        session_items.append({
            "word": w,
            "is_review": True,
            "frequency": r[7],
            "exam_count": r[8],
            "phonetic": r[9],
            "pos": r[10],
            "definition_zh": r[11],
            "examples": examples,
            "distractors": distractors,
            "srs": {
                "state": r[1],
                "stability": r[2],
                "difficulty": r[3],
                "reps": r[4],
                "lapses": r[5],
                "due": r[6]
            }
        })

    # Priority 2: Fill remaining quota with fresh new words
    if remaining_new_quota > 0:
        cursor.execute("""
            SELECT
                vf.word, vf.frequency, vf.exam_count, vf.phonetic, vf.pos, vf.definition_zh,
                vf.examples_json, vd.distractors_json
            FROM vocab_frequency vf
            LEFT JOIN user_vocab_srs uvs ON vf.word = uvs.word AND uvs.user_id = ?
            LEFT JOIN vocab_distractors vd ON vf.word = vd.word
            WHERE uvs.word IS NULL OR uvs.reps = 0
            ORDER BY vf.frequency DESC, vf.exam_count DESC
            LIMIT ?;
        """, (user_id, remaining_new_quota))
        new_rows = cursor.fetchall()

        for r in new_rows:
            w = r[0]
            if w in seen_words: continue
            seen_words.add(w)
            examples = json.loads(r[6] or "[]")
            distractors = json.loads(r[7] or "[]")
            session_items.append({
                "word": w,
                "is_review": False,
                "frequency": r[1],
                "exam_count": r[2],
                "phonetic": r[3],
                "pos": r[4],
                "definition_zh": r[5],
                "examples": examples,
                "distractors": distractors,
                "srs": {
                    "state": "new",
                    "stability": 0.0,
                    "difficulty": 0.0,
                    "reps": 0,
                    "lapses": 0,
                    "due": 0.0
                }
            })

    conn.close()

    return {
        "items": session_items,
        "due_count": len(due_rows),
        "new_count": len(session_items) - len(due_rows),
        "remaining_new_quota": remaining_new_quota,
        "is_completed": len(session_items) == 0
    }

@router.post("/card/rate")
def rate_vocab_card(req: RateCardRequest, current_user: dict = Depends(get_current_user_optional)):
    """
    Rates card via FSRS-5:
    rating:
      1: Again (不会 / 测验错误)
      2: Hard (模糊)
      3: Good (会了 + 听辨四选一测验正确)
    """
    if req.rating not in (1, 2, 3):
        raise HTTPException(status_code=400, detail="Rating must be 1 (Again), 2 (Hard), or 3 (Good)")

    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]
    clean_w = req.word.strip().lower()
    now = time.time()

    # Load existing SRS card
    cursor.execute("""
        SELECT state, stability, difficulty, reps, lapses, last_review, due, quiz_fails
        FROM user_vocab_srs WHERE user_id = ? AND word = ?;
    """, (user_id, clean_w))
    row = cursor.fetchone()

    if row:
        card = {
            "word": clean_w,
            "state": row[0],
            "stability": row[1],
            "difficulty": row[2],
            "reps": row[3],
            "lapses": row[4],
            "last_review": row[5],
            "due": row[6],
        }
        quiz_fails = row[7]
    else:
        card = fsrs.init_card(clean_w)
        quiz_fails = 0

    if req.quiz_passed is False:
        quiz_fails += 1

    # Schedule via FSRS-5
    updated = fsrs.schedule_card(card, req.rating, now)

    # Save to user_vocab_srs
    cursor.execute("""
        INSERT INTO user_vocab_srs (
            user_id, word, state, stability, difficulty, reps, lapses,
            last_review, due, rating, quiz_fails, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, word) DO UPDATE SET
            state = excluded.state,
            stability = excluded.stability,
            difficulty = excluded.difficulty,
            reps = excluded.reps,
            lapses = excluded.lapses,
            last_review = excluded.last_review,
            due = excluded.due,
            rating = excluded.rating,
            quiz_fails = excluded.quiz_fails,
            updated_at = excluded.updated_at;
    """, (
        user_id, clean_w, updated["state"], updated["stability"], updated["difficulty"],
        updated["reps"], updated["lapses"], updated["last_review"], updated["due"],
        req.rating, quiz_fails, now
    ))

    # Sync to legacy user_vocab_status for compatibility
    legacy_status = "known" if req.rating == 3 else "learning"
    cursor.execute("""
        INSERT INTO user_vocab_status (user_id, word, status, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, word) DO UPDATE SET
            status = excluded.status,
            updated_at = excluded.updated_at;
    """, (user_id, clean_w, legacy_status, now))

    # Log telemetry event
    evt_name = "rate_again" if req.rating == 1 else ("rate_hard" if req.rating == 2 else "rate_good")
    cursor.execute("""
        INSERT INTO vocab_events (user_id, event_name, word, payload_json, created_at)
        VALUES (?, ?, ?, ?, ?);
    """, (
        user_id, evt_name, clean_w,
        json.dumps({
            "rating": req.rating,
            "quiz_passed": req.quiz_passed,
            "stability": updated["stability"],
            "interval_days": updated["interval_days"],
            "listen_count": req.listen_count
        }),
        now
    ))

    conn.commit()
    conn.close()

    return {
        "status": "ok",
        "card": updated
    }

@router.post("/events")
def log_vocab_event(req: TelemetryEventRequest, current_user: dict = Depends(get_current_user_optional)):
    """Logs minimal user event for algorithm tuning."""
    conn = get_connection()
    cursor = conn.cursor()
    user_id = current_user["id"]
    now = time.time()

    cursor.execute("""
        INSERT INTO vocab_events (user_id, event_name, word, payload_json, created_at)
        VALUES (?, ?, ?, ?, ?);
    """, (user_id, req.event_name, req.word or "", json.dumps(req.payload or {}), now))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@router.delete("/{vocab_id}")
def delete_vocabulary(vocab_id: str, current_user: dict = Depends(get_current_user_optional)):
    """Delete a user vocabulary bookmark."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vocabulary WHERE id = ? AND user_id = ?", (vocab_id, current_user["id"]))
    conn.commit()
    conn.close()
    return {"status": "deleted"}
