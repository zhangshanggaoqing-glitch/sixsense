import time
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
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=30)
    password: str = Field(..., min_length=6, max_length=64)
    migrate_guest: Optional[bool] = True

class LoginRequest(BaseModel):
    username: str
    password: str
    migrate_guest: Optional[bool] = False

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

    # Optional: migrate guest vocabulary to this new registered user
    if req.migrate_guest:
        cursor.execute("UPDATE vocabulary SET user_id = ? WHERE user_id = 'default'", (user_id,))

    conn.commit()
    conn.close()

    token = create_access_token(user_id, clean_username)
    return {
        "status": "success",
        "token": token,
        "user": {
            "id": user_id,
            "username": clean_username,
            "created_at": now
        }
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

    # Optional: migrate guest vocabulary to this logged in account if user had added words
    if req.migrate_guest:
        cursor.execute("UPDATE vocabulary SET user_id = ? WHERE user_id = 'default'", (user_id,))

    conn.commit()
    conn.close()

    token = create_access_token(user_id, username)
    return {
        "status": "success",
        "token": token,
        "user": {
            "id": user_id,
            "username": username,
            "created_at": user["created_at"]
        }
    }

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user_required)):
    return {
        "status": "success",
        "user": {
            "id": current_user["id"],
            "username": current_user["username"],
            "created_at": current_user.get("created_at")
        }
    }
