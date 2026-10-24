import time
import json
import uuid
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.app.database import get_connection
from backend.app.utils.diff import compute_dictation_diff
from backend.app.utils.auth import get_current_user_optional

router = APIRouter(prefix="/api/progress", tags=["Progress & State"])

class ResumeStateRequest(BaseModel):
    exam_id: str
    section_id: Optional[str] = ""
    subpart_id: Optional[str] = ""
    sentence_index: int
    playback_rate: Optional[float] = 1.0
    display_mode: Optional[str] = "C"
    loop_mode: Optional[str] = "off"
    volume: Optional[float] = 1.0

class DictationCheckRequest(BaseModel):
    sentence_id: str
    standard_text: str
    user_input: str

class HeartbeatRequest(BaseModel):
    exam_id: str
    active_seconds: int

@router.get("/resume")
def get_resume(current_user: dict = Depends(get_current_user_optional)):
    conn = get_connection()
    cursor = conn.cursor()
    user_key = f"resume:{current_user['id']}"
    cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (user_key,))
    row = cursor.fetchone()
    if not row and current_user["id"] != "default":
        # Fallback to default/last_resume if user hasn't saved a personal resume yet
        cursor.execute("SELECT value_json FROM user_state WHERE key = 'last_resume'")
        row = cursor.fetchone()
    conn.close()

    if row and row["value_json"]:
        return json.loads(row["value_json"])
    return {
        "exam_id": "2020-07-set1",
        "sentence_index": 0,
        "playback_rate": 1.0,
        "display_mode": "C",
        "loop_mode": "off",
        "volume": 1.0
    }

@router.post("/resume")
def save_resume(req: ResumeStateRequest, current_user: dict = Depends(get_current_user_optional)):
    conn = get_connection()
    cursor = conn.cursor()
    val_json = json.dumps(req.model_dump(), ensure_ascii=False)
    now = time.time()
    user_key = f"resume:{current_user['id']}"

    cursor.execute("""
        INSERT INTO user_state (key, value_json, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = excluded.updated_at;
    """, (user_key, val_json, now))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@router.post("/dictation/check")
def check_dictation(req: DictationCheckRequest, current_user: dict = Depends(get_current_user_optional)):
    diff_res = compute_dictation_diff(req.standard_text, req.user_input)
    user_id = current_user["id"]

    # Record attempt into database
    conn = get_connection()
    cursor = conn.cursor()
    att_id = f"att_{uuid.uuid4().hex[:10]}"
    cursor.execute("""
        INSERT INTO dictation_attempts (
            id, sentence_id, user_input, standard_text, accuracy_score, diff_json, created_at, user_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        att_id, req.sentence_id, req.user_input, req.standard_text,
        diff_res["accuracy_score"], json.dumps(diff_res, ensure_ascii=False), time.time(), user_id
    ))
    conn.commit()
    conn.close()

    return diff_res

@router.post("/heartbeat")
def record_heartbeat(req: HeartbeatRequest, current_user: dict = Depends(get_current_user_optional)):
    conn = get_connection()
    cursor = conn.cursor()
    today = time.strftime("%Y-%m-%d")
    key = f"{current_user['id']}:daily_active_{today}"

    cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (key,))
    row = cursor.fetchone()
    current_seconds = 0
    if row and row["value_json"]:
        try: current_seconds = int(row["value_json"])
        except: pass

    new_seconds = current_seconds + req.active_seconds
    cursor.execute("""
        INSERT INTO user_state (key, value_json, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = excluded.updated_at;
    """, (key, str(new_seconds), time.time()))
    conn.commit()
    conn.close()
    return {"today_active_seconds": new_seconds}

@router.get("/stats")
def get_stats(current_user: dict = Depends(get_current_user_optional)):
    conn = get_connection()
    cursor = conn.cursor()
    today = time.strftime("%Y-%m-%d")
    user_id = current_user["id"]
    key = f"{user_id}:daily_active_{today}"

    cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (key,))
    row = cursor.fetchone()
    today_active = int(row["value_json"]) if row and row["value_json"] else 0

    cursor.execute("SELECT COUNT(*) as cnt FROM vocabulary WHERE user_id = ?", (user_id,))
    vocab_count = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) as cnt FROM dictation_attempts WHERE user_id = ?", (user_id,))
    dict_count = cursor.fetchone()["cnt"]

    conn.close()
    return {
        "today_minutes": round(today_active / 60, 1),
        "this_week_minutes": round(today_active / 60, 1),
        "streak_days": 1 if today_active > 0 else 0,
        "vocab_count": vocab_count,
        "dictation_count": dict_count
    }
