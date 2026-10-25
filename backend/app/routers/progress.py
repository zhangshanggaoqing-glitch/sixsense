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
    has_progress: Optional[bool] = False
    is_completed: Optional[bool] = False

class DictationCheckRequest(BaseModel):
    sentence_id: str
    standard_text: str
    user_input: str

class HeartbeatRequest(BaseModel):
    exam_id: str
    active_seconds: int
    completed_sentence: Optional[bool] = False

from datetime import datetime, timezone, timedelta

def get_cst_now() -> datetime:
    """Return current datetime in Asia/Shanghai timezone (UTC+8)."""
    cst = timezone(timedelta(hours=8))
    return datetime.now(cst)

def get_cst_today_str() -> str:
    """Return YYYY-MM-DD in Asia/Shanghai timezone (UTC+8)."""
    return get_cst_now().strftime("%Y-%m-%d")

def calculate_streak(cursor, user_id: str, today_active: int, now: datetime) -> int:
    """
    计算连续精听打卡天数（时区：Asia/Shanghai）。
    规则：
    1. 当天有效精听 >= 60 秒（1 分钟）记为有效打卡日。
    2. 若今日已达标 (today_active >= 60)：连续天数 = 1 + 往前回溯连续达标天数。
    3. 若今日尚未达标 (today_active < 60)：
       - 检查昨日是否达标。若昨日达标，则保持昨日的连续打卡天数（今日达标后将 +1）；
       - 若昨日未达标，则判定已断签，连续天数归 0（下次达标从 1 重新起算）。
    """
    yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (f"{user_id}:daily_active_{yesterday_str}",))
    y_row = cursor.fetchone()
    yesterday_active = int(y_row["value_json"]) if y_row and y_row["value_json"] and y_row["value_json"].isdigit() else 0

    if today_active >= 60:
        streak_days = 1
        for i in range(1, 365):
            d_str = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (f"{user_id}:daily_active_{d_str}",))
            r = cursor.fetchone()
            if r and r["value_json"] and r["value_json"].isdigit() and int(r["value_json"]) >= 60:
                streak_days += 1
            else:
                break
        return streak_days
    elif yesterday_active >= 60:
        streak_days = 1
        for i in range(2, 365):
            d_str = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (f"{user_id}:daily_active_{d_str}",))
            r = cursor.fetchone()
            if r and r["value_json"] and r["value_json"].isdigit() and int(r["value_json"]) >= 60:
                streak_days += 1
            else:
                break
        return streak_days
    else:
        return 0

def evaluate_medals(cursor, user_id: str, streak_days: int, completed_sentence: bool = False) -> tuple[list[str], list[str]]:
    """
    评估并点亮勋章（最多仅 3 枚，静默权威判定）：
    1. first_listen: 完成至少 1 句有效播放（听完 1 句 或 累计播放时长 >= 15s）
    2. streak_3: 连续精听 >= 3 天
    3. streak_7: 连续精听 >= 7 天
    返回：(当前所有已拥有勋章列表, 本次新点亮的勋章列表)
    """
    key = f"medals:{user_id}"
    cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (key,))
    row = cursor.fetchone()
    current_medals: list[str] = []
    if row and row["value_json"]:
        try:
            current_medals = json.loads(row["value_json"])
        except Exception:
            current_medals = []

    new_medals: list[str] = []

    # 1. first_listen
    if "first_listen" not in current_medals:
        if completed_sentence:
            new_medals.append("first_listen")
        else:
            cursor.execute("SELECT SUM(active_seconds) as total_sec FROM listening_sessions WHERE user_id = ?", (user_id,))
            tot_row = cursor.fetchone()
            if tot_row and tot_row["total_sec"] and tot_row["total_sec"] >= 15:
                new_medals.append("first_listen")

    # 2. streak_3
    if "streak_3" not in current_medals and streak_days >= 3:
        new_medals.append("streak_3")

    # 3. streak_7
    if "streak_7" not in current_medals and streak_days >= 7:
        new_medals.append("streak_7")

    if new_medals:
        all_medals = current_medals + new_medals
        now_ts = time.time()
        cursor.execute("""
            INSERT INTO user_state (key, value_json, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = excluded.updated_at;
        """, (key, json.dumps(all_medals, ensure_ascii=False), now_ts))
        return all_medals, new_medals

    return current_medals, []

@router.get("/resume")
def get_resume(current_user: dict = Depends(get_current_user_optional)):
    conn = get_connection()
    cursor = conn.cursor()
    user_key = f"resume:{current_user['id']}"
    cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (user_key,))
    row = cursor.fetchone()

    # If the user or guest has their own saved resume, return it immediately
    if row and row["value_json"]:
        conn.close()
        try:
            return json.loads(row["value_json"])
        except Exception:
            pass
    else:
        conn.close()

    # Default to latest exam and first subpart in database, bilingual mode
    latest_exam_id = "2026-06-set1"
    latest_subpart_id = "2026-06-set1-conv-1"
    try:
        conn2 = get_connection()
        c2 = conn2.cursor()
        c2.execute("SELECT id FROM exams ORDER BY year DESC, month DESC, set_number ASC LIMIT 1")
        ex_row = c2.fetchone()
        if ex_row:
            latest_exam_id = ex_row["id"]
            c2.execute("SELECT id FROM subparts WHERE exam_id = ? ORDER BY order_num ASC LIMIT 1", (latest_exam_id,))
            sp_row = c2.fetchone()
            if sp_row:
                latest_subpart_id = sp_row["id"]
        conn2.close()
    except Exception:
        pass

    return {
        "exam_id": latest_exam_id,
        "subpart_id": latest_subpart_id,
        "sentence_index": 0,
        "playback_rate": 1.0,
        "display_mode": "A",
        "loop_mode": "off",
        "volume": 1.0,
        "has_progress": False,
        "is_completed": False
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
    if req.active_seconds <= 0:
        return {"status": "ok", "active_seconds": 0}

    # Clamp active_seconds per request (max 120s) to guard against erratic time jumps
    clamped_seconds = min(req.active_seconds, 120)
    user_id = current_user["id"]
    now_ts = time.time()
    cst_now = get_cst_now()
    today_str = cst_now.strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    # 1. Update / Insert into listening_sessions (used by admin analytics & streak)
    # Check if there is an active session in the last 5 minutes (300s) for this user & exam
    cursor.execute("""
        SELECT id, active_seconds FROM listening_sessions 
        WHERE user_id = ? AND exam_id = ? AND end_time >= ?
        ORDER BY end_time DESC LIMIT 1
    """, (user_id, req.exam_id, now_ts - 300))
    recent_sess = cursor.fetchone()

    if recent_sess:
        sess_id = recent_sess["id"]
        cursor.execute("""
            UPDATE listening_sessions 
            SET end_time = ?, active_seconds = active_seconds + ?
            WHERE id = ?
        """, (now_ts, clamped_seconds, sess_id))
    else:
        sess_id = f"sess_{uuid.uuid4().hex[:12]}"
        cursor.execute("""
            INSERT INTO listening_sessions (
                id, start_time, end_time, active_seconds, exam_id, user_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (sess_id, now_ts - clamped_seconds, now_ts, clamped_seconds, req.exam_id, user_id))

    # 2. Update user_state daily active counter (Asia/Shanghai)
    key = f"{user_id}:daily_active_{today_str}"
    cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (key,))
    row = cursor.fetchone()
    current_seconds = 0
    if row and row["value_json"]:
        try:
            current_seconds = int(row["value_json"])
        except Exception:
            pass

    new_seconds = current_seconds + clamped_seconds
    cursor.execute("""
        INSERT INTO user_state (key, value_json, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = excluded.updated_at;
    """, (key, str(new_seconds), now_ts))

    # 3. Calculate streak and evaluate medals
    streak_days = calculate_streak(cursor, user_id, new_seconds, cst_now)
    all_medals, new_medals = evaluate_medals(cursor, user_id, streak_days, completed_sentence=bool(req.completed_sentence))

    conn.commit()
    conn.close()
    return {
        "status": "ok",
        "today_active_seconds": new_seconds,
        "today_minutes": round(new_seconds / 60.0, 1),
        "streak_days": streak_days,
        "medals": all_medals,
        "new_medals": new_medals
    }

@router.get("/stats")
def get_stats(current_user: dict = Depends(get_current_user_optional)):
    conn = get_connection()
    cursor = conn.cursor()
    cst_now = get_cst_now()
    today_str = cst_now.strftime("%Y-%m-%d")
    user_id = current_user["id"]
    key = f"{user_id}:daily_active_{today_str}"

    cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (key,))
    row = cursor.fetchone()
    today_active = int(row["value_json"]) if row and row["value_json"] and row["value_json"].isdigit() else 0

    # Weekly active seconds (Monday to today in CST)
    weekday = cst_now.weekday()
    monday = cst_now - timedelta(days=weekday)
    week_keys = [f"{user_id}:daily_active_{(monday + timedelta(days=d)).strftime('%Y-%m-%d')}" for d in range(weekday + 1)]
    placeholders = ",".join("?" for _ in week_keys)
    cursor.execute(f"SELECT value_json FROM user_state WHERE key IN ({placeholders})", week_keys)
    week_rows = cursor.fetchall()
    this_week_seconds = sum(int(r["value_json"]) for r in week_rows if r["value_json"] and r["value_json"].isdigit())

    # Streak calculation
    streak_days = calculate_streak(cursor, user_id, today_active, cst_now)

    # Medals
    all_medals, _ = evaluate_medals(cursor, user_id, streak_days, completed_sentence=False)

    cursor.execute("SELECT COUNT(*) as cnt FROM vocabulary WHERE user_id = ?", (user_id,))
    vocab_count = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) as cnt FROM dictation_attempts WHERE user_id = ?", (user_id,))
    dict_count = cursor.fetchone()["cnt"]

    conn.close()
    return {
        "today_minutes": round(today_active / 60.0, 1),
        "this_week_minutes": round(max(this_week_seconds, today_active) / 60.0, 1),
        "streak_days": streak_days,
        "vocab_count": vocab_count,
        "dictation_count": dict_count,
        "medals": all_medals
    }
