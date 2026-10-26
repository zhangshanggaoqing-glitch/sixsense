import time
import os
import re
import gzip
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any, Set
from fastapi import APIRouter, Depends, Query
from backend.app.database import get_connection
from backend.app.utils.auth import get_current_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin Dashboard"])

# Strict Asia/Shanghai timezone (China Standard Time, UTC+8)
CST = timezone(timedelta(hours=8))

def get_today_midnight_ts() -> float:
    """
    Return UNIX timestamp for today's midnight (00:00:00) in Asia/Shanghai timezone.
    All 'today' metrics strictly align to this day-cut boundary.
    """
    now = datetime.now(CST)
    today_start = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=CST)
    return today_start.timestamp()

# In-memory short cache for traffic parsing (15s TTL) to prevent disk I/O on rapid requests
_traffic_cache: Dict[str, Any] = {"ts": 0.0, "data": None}

def get_traffic_metrics(conn=None) -> Dict[str, int]:
    """
    Calculate real-time PV and unique visitor IPs (UV) from Nginx access logs.
    
    Guarantees:
    1. Day-cut strictly uses Asia/Shanghai (00:00:00 CST).
    2. Monotonicity: Cumulative PV and UV never decrease, even across Nginx logrotate,
       server restarts, or log purges.
    3. Excludes internal developer/server IPs and internal private network (100.*).
    4. Past daily counts and discovered IPs are safely persisted into `user_state`.
    """
    now_ts = time.time()
    if _traffic_cache["data"] is not None and (now_ts - _traffic_cache["ts"]) < 15.0:
        return _traffic_cache["data"]

    close_conn_here = False
    if conn is None:
        conn = get_connection()
        close_conn_here = True

    cursor = conn.cursor()

    # 1. Load persisted baseline / high-water marks from SQLite user_state
    persisted: Dict[str, Any] = {}
    try:
        cursor.execute("SELECT value_json FROM user_state WHERE key = 'admin:traffic_metrics'")
        row = cursor.fetchone()
        if row and row["value_json"]:
            persisted = json.loads(row["value_json"])
    except Exception as e:
        print("[Admin Traffic] Failed to load persisted state:", e)

    # 2. Identify all available Nginx access log files (including rotated and gzipped)
    candidate_dirs = [
        Path("/var/log/nginx"),
        Path("/app/data"),
        Path("/home/ubuntu/sixsense/data"),
    ]
    log_files: List[Path] = []
    for cdir in candidate_dirs:
        if cdir.exists() and cdir.is_dir():
            found = sorted(cdir.glob("access.log*")) or sorted(cdir.glob("nginx_access*"))
            if found:
                log_files = found
                break

    dev_ips = {"129.146.129.236", "127.0.0.1", "161.153.13.244"}
    now_cst = datetime.now(CST)
    today_cst_date = now_cst.date()

    log_total_pv = 0
    log_all_ips: Set[str] = set()
    today_pv = 0
    today_ips: Set[str] = set()
    daily_pv: Dict[str, int] = {}

    if log_files:
        for p in log_files:
            open_fn = gzip.open if p.name.endswith(".gz") else open
            try:
                with open_fn(p, "rt", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        log_total_pv += 1
                        bracket_idx = line.find("[")
                        if bracket_idx == -1:
                            continue
                        ip = line[:bracket_idx].split()[0]
                        if ip in dev_ips or ip.startswith("100."):
                            continue

                        log_all_ips.add(ip)
                        end_bracket = line.find("]", bracket_idx)
                        if end_bracket != -1:
                            t_str = line[bracket_idx + 1:end_bracket]
                            try:
                                dt = datetime.strptime(t_str, "%d/%b/%Y:%H:%M:%S %z")
                                d_cst = dt.astimezone(CST).date()
                                d_key = str(d_cst)
                                daily_pv[d_key] = daily_pv.get(d_key, 0) + 1
                                if d_cst == today_cst_date:
                                    today_pv += 1
                                    today_ips.add(ip)
                            except Exception:
                                pass
            except Exception as e:
                print(f"[Admin Traffic] Failed to read {p}:", e)

    # 3. Merge with historical persisted daily counts and known IPs
    historical_daily_pv: Dict[str, int] = persisted.get("daily_pv", {})
    # For all closed days strictly before today, store maximum recorded PV in SQLite
    for d_str, count in daily_pv.items():
        if d_str < str(today_cst_date):
            historical_daily_pv[d_str] = max(historical_daily_pv.get(d_str, 0), count)

    computed_past_pv = sum(historical_daily_pv.values())
    total_pv = max(computed_past_pv + today_pv, log_total_pv, persisted.get("highest_total_pv", 0))

    # Merge IP sets to guarantee total_uv never decreases
    known_ips = set(persisted.get("known_ips", []))
    known_ips.update(log_all_ips)
    total_uv = max(len(known_ips), persisted.get("highest_total_uv", 0))
    today_uv = len(today_ips)

    # 4. Save updated high-water marks and historical daily counts into user_state
    try:
        to_store = {
            "highest_total_pv": total_pv,
            "highest_total_uv": total_uv,
            "daily_pv": historical_daily_pv,
            "known_ips": list(known_ips)[:25000],  # Keep IP set compact
            "updated_at": now_ts,
        }
        cursor.execute("""
            INSERT INTO user_state (key, value_json, updated_at)
            VALUES ('admin:traffic_metrics', ?, ?)
            ON CONFLICT(key) DO UPDATE SET 
                value_json = excluded.value_json, 
                updated_at = excluded.updated_at
        """, (json.dumps(to_store), now_ts))
        conn.commit()
    except Exception as e:
        print("[Admin Traffic] Failed to persist state into user_state:", e)

    if close_conn_here:
        conn.close()

    result = {
        "total_pv": total_pv,
        "total_uv": total_uv,
        "today_pv": today_pv,
        "today_uv": today_uv,
    }
    _traffic_cache["ts"] = now_ts
    _traffic_cache["data"] = result
    return result

@router.get("/overview")
def get_overview(admin: dict = Depends(get_current_admin_user)):
    """
    Admin dashboard overview API.
    All daily metrics are partitioned strictly by Asia/Shanghai (00:00:00 CST).
    Listening, vocab, and dictation numbers are partitioned into:
    - Total = Registered + Guest
    - Today = Registered + Guest
    """
    conn = get_connection()
    cursor = conn.cursor()
    today_ts = get_today_midnight_ts()

    # 1. Traffic stats (PV & UV)
    traffic = get_traffic_metrics(conn)

    # 2. User stats
    cursor.execute("SELECT COUNT(*) as count FROM users")
    total_users = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM users WHERE created_at >= ?", (today_ts,))
    today_new_users = cursor.fetchone()["count"]

    # Registered active users today: registered users with last_login_at >= today_ts OR active listening sessions today
    cursor.execute("""
        SELECT COUNT(DISTINCT id) as count 
        FROM users 
        WHERE last_login_at >= ? 
           OR id IN (SELECT user_id FROM listening_sessions WHERE end_time >= ?)
    """, (today_ts, today_ts))
    active_users_today = cursor.fetchone()["count"]

    # 3. Listening stats (Strictly partitioned into Registered vs Guest)
    cursor.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN user_id LIKE 'usr_%' THEN active_seconds ELSE 0 END), 0) / 60.0 as reg_min,
            COALESCE(SUM(CASE WHEN user_id NOT LIKE 'usr_%' THEN active_seconds ELSE 0 END), 0) / 60.0 as gst_min
        FROM listening_sessions
    """)
    listen_row = cursor.fetchone()
    registered_listening_minutes = round(listen_row["reg_min"] or 0, 1)
    guest_listening_minutes = round(listen_row["gst_min"] or 0, 1)
    total_listening_minutes = round(registered_listening_minutes + guest_listening_minutes, 1)

    cursor.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN user_id LIKE 'usr_%' THEN active_seconds ELSE 0 END), 0) / 60.0 as reg_min,
            COALESCE(SUM(CASE WHEN user_id NOT LIKE 'usr_%' THEN active_seconds ELSE 0 END), 0) / 60.0 as gst_min
        FROM listening_sessions 
        WHERE end_time >= ?
    """, (today_ts,))
    today_listen_row = cursor.fetchone()
    today_registered_listening_minutes = round(today_listen_row["reg_min"] or 0, 1)
    today_guest_listening_minutes = round(today_listen_row["gst_min"] or 0, 1)
    today_listening_minutes = round(today_registered_listening_minutes + today_guest_listening_minutes, 1)

    # 4. Vocabulary stats (Total, Registered, Guest)
    cursor.execute("""
        SELECT 
            COUNT(*) as total_count,
            SUM(CASE WHEN user_id LIKE 'usr_%' THEN 1 ELSE 0 END) as reg_count,
            SUM(CASE WHEN user_id NOT LIKE 'usr_%' THEN 1 ELSE 0 END) as gst_count
        FROM vocabulary
    """)
    vocab_row = cursor.fetchone()
    total_vocab_words = vocab_row["total_count"] or 0
    registered_vocab_words = vocab_row["reg_count"] or 0
    guest_vocab_words = vocab_row["gst_count"] or 0

    cursor.execute("""
        SELECT 
            COUNT(*) as total_count,
            SUM(CASE WHEN user_id LIKE 'usr_%' THEN 1 ELSE 0 END) as reg_count,
            SUM(CASE WHEN user_id NOT LIKE 'usr_%' THEN 1 ELSE 0 END) as gst_count
        FROM vocabulary 
        WHERE created_at >= ?
    """, (today_ts,))
    today_vocab_row = cursor.fetchone()
    today_vocab_words = today_vocab_row["total_count"] or 0
    today_registered_vocab_words = today_vocab_row["reg_count"] or 0
    today_guest_vocab_words = today_vocab_row["gst_count"] or 0

    # 5. Dictation stats (Total, Registered, Guest)
    cursor.execute("""
        SELECT 
            COUNT(*) as total_count,
            SUM(CASE WHEN user_id LIKE 'usr_%' THEN 1 ELSE 0 END) as reg_count,
            SUM(CASE WHEN user_id NOT LIKE 'usr_%' THEN 1 ELSE 0 END) as gst_count,
            COALESCE(AVG(accuracy_score), 0) as avg_score 
        FROM dictation_attempts
    """)
    dict_row = cursor.fetchone()
    total_dictation_attempts = dict_row["total_count"] or 0
    registered_dictation_attempts = dict_row["reg_count"] or 0
    guest_dictation_attempts = dict_row["gst_count"] or 0
    avg_dictation_accuracy = round((dict_row["avg_score"] or 0) * 100, 1)

    cursor.execute("""
        SELECT 
            COUNT(*) as total_count,
            SUM(CASE WHEN user_id LIKE 'usr_%' THEN 1 ELSE 0 END) as reg_count,
            SUM(CASE WHEN user_id NOT LIKE 'usr_%' THEN 1 ELSE 0 END) as gst_count
        FROM dictation_attempts 
        WHERE created_at >= ?
    """, (today_ts,))
    today_dict_row = cursor.fetchone()
    today_dictation_attempts = today_dict_row["total_count"] or 0
    today_registered_dictation_attempts = today_dict_row["reg_count"] or 0
    today_guest_dictation_attempts = today_dict_row["gst_count"] or 0

    conn.close()

    return {
        "status": "success",
        "data": {
            # Traffic
            "total_pv": traffic["total_pv"],
            "total_uv": traffic["total_uv"],
            "today_pv": traffic["today_pv"],
            "today_uv": traffic["today_uv"],
            # Users
            "total_users": total_users,
            "today_new_users": today_new_users,
            "active_users_today": active_users_today,
            # Listening
            "total_listening_minutes": total_listening_minutes,
            "registered_listening_minutes": registered_listening_minutes,
            "guest_listening_minutes": guest_listening_minutes,
            "today_listening_minutes": today_listening_minutes,
            "today_registered_listening_minutes": today_registered_listening_minutes,
            "today_guest_listening_minutes": today_guest_listening_minutes,
            # Vocabulary
            "total_vocab_words": total_vocab_words,
            "registered_vocab_words": registered_vocab_words,
            "guest_vocab_words": guest_vocab_words,
            "today_vocab_words": today_vocab_words,
            "today_registered_vocab_words": today_registered_vocab_words,
            "today_guest_vocab_words": today_guest_vocab_words,
            # Dictation
            "total_dictation_attempts": total_dictation_attempts,
            "registered_dictation_attempts": registered_dictation_attempts,
            "guest_dictation_attempts": guest_dictation_attempts,
            "today_dictation_attempts": today_dictation_attempts,
            "today_registered_dictation_attempts": today_registered_dictation_attempts,
            "today_guest_dictation_attempts": today_guest_dictation_attempts,
            "avg_dictation_accuracy": avg_dictation_accuracy,
        }
    }

@router.get("/users")
def get_users(
    q: Optional[str] = Query(None, description="Search query by username"),
    admin: dict = Depends(get_current_admin_user)
):
    """
    List all registered users with their individual stats.
    The sum of listening_minutes across all rows matches registered_listening_minutes.
    """
    conn = get_connection()
    cursor = conn.cursor()
    today_ts = get_today_midnight_ts()

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
    total_reg_listen = 0.0
    total_reg_vocab = 0
    total_reg_dict = 0
    for r in rows:
        lm = round(r["listening_minutes"] or 0, 1)
        vc = r["vocab_count"] or 0
        dc = r["dictation_count"] or 0
        total_reg_listen += lm
        total_reg_vocab += vc
        total_reg_dict += dc
        users_list.append({
            "id": r["id"],
            "username": r["username"],
            "created_at": r["created_at"],
            "last_login_at": r["last_login_at"],
            "vocab_count": vc,
            "listening_minutes": lm,
            "dictation_count": dc,
        })

    return {
        "status": "success",
        "total": len(users_list),
        "total_listening_minutes": round(total_reg_listen, 1),
        "total_vocab_count": total_reg_vocab,
        "total_dictation_count": total_reg_dict,
        "today_ts": today_ts,
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
