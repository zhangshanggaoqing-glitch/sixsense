import time
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query
from backend.app.database import get_connection
from backend.app.utils.auth import get_current_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin Dashboard"])

def get_today_midnight_ts() -> float:
    """Return UNIX timestamp for today's midnight in UTC+8 (China Standard Time)."""
    cst = timezone(timedelta(hours=8))
    now = datetime.now(cst)
    today_start = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=cst)
    return today_start.timestamp()

@router.get("/overview")
def get_overview(admin: dict = Depends(get_current_admin_user)):
    conn = get_connection()
    cursor = conn.cursor()
    today_ts = get_today_midnight_ts()

    # 1. User stats
    cursor.execute("SELECT COUNT(*) as count FROM users")
    total_users = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM users WHERE created_at >= ?", (today_ts,))
    today_new_users = cursor.fetchone()["count"]

    cursor.execute("""
        SELECT COUNT(DISTINCT user_id) as count 
        FROM listening_sessions 
        WHERE end_time >= ? AND user_id != 'default'
    """, (today_ts,))
    active_users_today = cursor.fetchone()["count"]

    # Also consider users who logged in today as active
    cursor.execute("""
        SELECT COUNT(*) as count 
        FROM users 
        WHERE last_login_at >= ?
    """, (today_ts,))
    login_users_today = cursor.fetchone()["count"]
    active_users_today = max(active_users_today, login_users_today)

    # 2. Listening stats
    cursor.execute("SELECT COALESCE(SUM(active_seconds), 0) / 60.0 as minutes FROM listening_sessions")
    total_listening_minutes = round(cursor.fetchone()["minutes"], 1)

    cursor.execute("SELECT COALESCE(SUM(active_seconds), 0) / 60.0 as minutes FROM listening_sessions WHERE end_time >= ?", (today_ts,))
    today_listening_minutes = round(cursor.fetchone()["minutes"], 1)

    # 3. Vocabulary stats
    cursor.execute("SELECT COUNT(*) as count FROM vocabulary")
    total_vocab_words = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM vocabulary WHERE created_at >= ?", (today_ts,))
    today_vocab_words = cursor.fetchone()["count"]

    # 4. Dictation stats
    cursor.execute("SELECT COUNT(*) as count, COALESCE(AVG(accuracy_score), 0) as avg_score FROM dictation_attempts")
    dict_row = cursor.fetchone()
    total_dictation_attempts = dict_row["count"]
    avg_dictation_accuracy = round(dict_row["avg_score"] * 100, 1)

    conn.close()

    return {
        "status": "success",
        "data": {
            "total_users": total_users,
            "today_new_users": today_new_users,
            "active_users_today": active_users_today,
            "total_listening_minutes": total_listening_minutes,
            "today_listening_minutes": today_listening_minutes,
            "total_vocab_words": total_vocab_words,
            "today_vocab_words": today_vocab_words,
            "total_dictation_attempts": total_dictation_attempts,
            "avg_dictation_accuracy": avg_dictation_accuracy
        }
    }

@router.get("/users")
def get_users(
    q: Optional[str] = Query(None, description="Search query by username"),
    admin: dict = Depends(get_current_admin_user)
):
    conn = get_connection()
    cursor = conn.cursor()

    query_str = """
        SELECT 
            u.id, 
            u.username, 
            u.created_at, 
            u.last_login_at,
            (SELECT COUNT(*) FROM vocabulary v WHERE v.user_id = u.id) as vocab_count,
            (SELECT COALESCE(SUM(s.active_seconds), 0) / 60.0 FROM listening_sessions s WHERE s.user_id = u.id) as listening_minutes,
            (SELECT COUNT(*) FROM dictation_attempts d WHERE d.user_id = u.id) as dictation_count
        FROM users u
    """
    params = []
    if q and q.strip():
        query_str += " WHERE LOWER(u.username) LIKE ?"
        params.append(f"%{q.strip().lower()}%")

    query_str += " ORDER BY u.created_at DESC"

    cursor.execute(query_str, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    users_list = []
    for r in rows:
        users_list.append({
            "id": r["id"],
            "username": r["username"],
            "created_at": r["created_at"],
            "last_login_at": r["last_login_at"],
            "vocab_count": r["vocab_count"] or 0,
            "listening_minutes": round(r["listening_minutes"] or 0, 1),
            "dictation_count": r["dictation_count"] or 0,
        })

    return {
        "status": "success",
        "total": len(users_list),
        "users": users_list
    }

@router.get("/popular-words")
def get_popular_words(limit: int = 15, admin: dict = Depends(get_current_admin_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            LOWER(word) as word_lower,
            word,
            part_of_speech,
            definition_zh,
            phonetic_uk,
            phonetic_us,
            COUNT(*) as save_count
        FROM vocabulary
        GROUP BY LOWER(word)
        ORDER BY save_count DESC, created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    words_list = []
    for r in rows:
        words_list.append({
            "word": r["word"],
            "part_of_speech": r["part_of_speech"] or "",
            "definition_zh": r["definition_zh"] or "",
            "phonetic_uk": r["phonetic_uk"] or "",
            "phonetic_us": r["phonetic_us"] or "",
            "count": r["save_count"]
        })

    return {
        "status": "success",
        "words": words_list
    }

@router.get("/popular-exams")
def get_popular_exams(limit: int = 10, admin: dict = Depends(get_current_admin_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            s.exam_id,
            COALESCE(e.title, s.exam_id) as title,
            COUNT(*) as session_count,
            ROUND(SUM(s.active_seconds) / 60.0, 1) as total_minutes
        FROM listening_sessions s
        LEFT JOIN exams e ON e.id = s.exam_id
        GROUP BY s.exam_id
        ORDER BY session_count DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    exams_list = []
    for r in rows:
        exams_list.append({
            "exam_id": r["exam_id"],
            "title": r["title"],
            "session_count": r["session_count"],
            "total_minutes": r["total_minutes"]
        })

    return {
        "status": "success",
        "exams": exams_list
    }
