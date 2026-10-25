import time
import json
import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from backend.app.database import get_connection
from backend.app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_required,
    get_current_user_optional,
    is_admin_user,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=30)
    password: str = Field(..., min_length=6, max_length=64)
    migrate_guest: Optional[bool] = True
    guest_id: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
    migrate_guest: Optional[bool] = False
    guest_id: Optional[str] = None

def _migrate_guest_data(cursor, guest_id: str, user_id: str, now: float):
    """
    将隔离访客数据平滑合并至正式账号：
    1. 迁移生词本、听力时长流水、听写记录
    2. 迁移播放进度记忆（resume）
    3. 迁移各自然日有效精听秒数（daily_active），避免今日精听跳 0
    4. 迁移并合并静默勋章成就（medals）
    """
    gid = guest_id.strip()
    if not gid or gid == "default" or gid == user_id:
        return

    cursor.execute("UPDATE vocabulary SET user_id = ? WHERE user_id = ?", (user_id, gid))
    cursor.execute("UPDATE listening_sessions SET user_id = ? WHERE user_id = ?", (user_id, gid))
    cursor.execute("UPDATE dictation_attempts SET user_id = ? WHERE user_id = ?", (user_id, gid))

    # 迁移 resume
    cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (f"resume:{gid}",))
    r_row = cursor.fetchone()
    if r_row:
        cursor.execute("""
            INSERT INTO user_state (key, value_json, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = excluded.updated_at
        """, (f"resume:{user_id}", r_row["value_json"], now))
        cursor.execute("DELETE FROM user_state WHERE key = ?", (f"resume:{gid}",))

    # 迁移 daily_active 记录（合并秒数，杜绝双计与归零）
    cursor.execute("SELECT key, value_json FROM user_state WHERE key LIKE ?", (f"{gid}:daily_active_%",))
    daily_rows = cursor.fetchall()
    for d_row in daily_rows:
        old_k = d_row["key"]
        date_suffix = old_k.split(":daily_active_")[-1]
        new_k = f"{user_id}:daily_active_{date_suffix}"
        guest_sec = int(d_row["value_json"]) if d_row["value_json"] and d_row["value_json"].isdigit() else 0

        cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (new_k,))
        u_row = cursor.fetchone()
        user_sec = int(u_row["value_json"]) if u_row and u_row["value_json"] and u_row["value_json"].isdigit() else 0
        merged_sec = user_sec + guest_sec

        cursor.execute("""
            INSERT INTO user_state (key, value_json, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = excluded.updated_at
        """, (new_k, str(merged_sec), now))
        cursor.execute("DELETE FROM user_state WHERE key = ?", (old_k,))

    # 迁移并合并 medals 勋章
    cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (f"medals:{gid}",))
    g_medals_row = cursor.fetchone()
    if g_medals_row and g_medals_row["value_json"]:
        try:
            g_medals = json.loads(g_medals_row["value_json"])
        except Exception:
            g_medals = []
        cursor.execute("SELECT value_json FROM user_state WHERE key = ?", (f"medals:{user_id}",))
        u_medals_row = cursor.fetchone()
        u_medals = []
        if u_medals_row and u_medals_row["value_json"]:
            try:
                u_medals = json.loads(u_medals_row["value_json"])
            except Exception:
                u_medals = []
        combined_medals = list(dict.fromkeys(u_medals + g_medals))
        cursor.execute("""
            INSERT INTO user_state (key, value_json, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = excluded.updated_at
        """, (f"medals:{user_id}", json.dumps(combined_medals, ensure_ascii=False), now))
        cursor.execute("DELETE FROM user_state WHERE key = ?", (f"medals:{gid}",))

@router.post("/register")
def register(req: RegisterRequest):
    clean_username = req.username.strip()
    if len(clean_username) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名长度至少为 2 个字符"
        )
    if len(req.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码长度至少为 6 个字符"
        )

    conn = get_connection()
    cursor = conn.cursor()

    # Check if username exists (case-insensitive)
    cursor.execute("SELECT id FROM users WHERE LOWER(username) = LOWER(?)", (clean_username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被注册，请直接登录"
        )

    user_id = f"usr_{uuid.uuid4().hex[:10]}"
    pw_hash = hash_password(req.password)
    now = time.time()

    cursor.execute("""
        INSERT INTO users (id, username, password_hash, created_at, last_login_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, clean_username, pw_hash, now, now))

    # Migrate guest data strictly bound to this guest_id (never touching other visitors)
    if req.migrate_guest and req.guest_id:
        _migrate_guest_data(cursor, req.guest_id, user_id, now)

    conn.commit()
    conn.close()

    token = create_access_token(user_id, clean_username)
    user_dict = {
        "id": user_id,
        "username": clean_username,
        "created_at": now,
        "is_admin": is_admin_user({"username": clean_username})
    }
    return {
        "status": "success",
        "token": token,
        "user": user_dict
    }

@router.post("/login")
def login(req: LoginRequest):
    clean_username = req.username.strip()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (clean_username,))
    user = cursor.fetchone()

    if not user or not verify_password(req.password, user["password_hash"]):
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    user_id = user["id"]
    username = user["username"]
    now = time.time()

    cursor.execute("UPDATE users SET last_login_at = ? WHERE id = ?", (now, user_id))

    # Migrate isolated guest data if guest_id provided
    if req.migrate_guest and req.guest_id:
        _migrate_guest_data(cursor, req.guest_id, user_id, now)

    conn.commit()
    conn.close()

    token = create_access_token(user_id, username)
    user_dict = {
        "id": user_id,
        "username": username,
        "created_at": user["created_at"],
        "is_admin": is_admin_user({"username": username})
    }
    return {
        "status": "success",
        "token": token,
        "user": user_dict
    }

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user_required)):
    return {
        "status": "success",
        "user": {
            "id": current_user["id"],
            "username": current_user["username"],
            "created_at": current_user.get("created_at"),
            "is_admin": current_user.get("is_admin", False)
        }
    }
