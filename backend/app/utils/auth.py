import os
import time
import secrets
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, status, Depends
import bcrypt
import jwt
from backend.app.config import DATA_DIR
from backend.app.database import get_connection

# JWT secret key management: read from env or persist to data/.jwt_secret
_SECRET_FILE = Path(DATA_DIR) / ".jwt_secret"
if os.getenv("JWT_SECRET"):
    JWT_SECRET = os.getenv("JWT_SECRET")
elif _SECRET_FILE.exists():
    try:
        JWT_SECRET = _SECRET_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        JWT_SECRET = secrets.token_hex(32)
else:
    JWT_SECRET = secrets.token_hex(32)
    try:
        _SECRET_FILE.parent.mkdir(parents=True, exist_ok=True)
        _SECRET_FILE.write_text(JWT_SECRET, encoding="utf-8")
    except Exception:
        pass

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 30 * 86400  # 30 days expiration for seamless study experience

def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    pw_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pw_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def create_access_token(user_id: str, username: str) -> str:
    """Create a signed JWT access token."""
    now = time.time()
    payload = {
        "sub": user_id,
        "username": username,
        "iat": int(now),
        "exp": int(now + ACCESS_TOKEN_EXPIRE_SECONDS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate a JWT access token."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except (jwt.PyJWTError, Exception):
        return None

ADMIN_USERNAMES = {"stone", "admin"}

def is_admin_user(user: Optional[Dict[str, Any]]) -> bool:
    if not user or user.get("is_guest"):
        return False
    username = user.get("username", "").strip().lower()
    return username in ADMIN_USERNAMES or user.get("is_admin") is True

import re

def _clean_guest_id(guest_id: Any) -> str:
    """
    Validate and sanitize client-provided guest UUID to prevent crosstalk or path issues.
    Ensures guest progress and stats stay strictly isolated per browser session.
    """
    if isinstance(guest_id, str):
        clean = guest_id.strip()
        if re.match(r"^gst_[a-zA-Z0-9_-]{8,64}$", clean):
            return clean
        if re.match(r"^[a-zA-Z0-9_-]{8,64}$", clean):
            return f"gst_{clean}"
    return "default"

def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    x_guest_id: Optional[str] = Header(None)
) -> Dict[str, Any]:
    """
    Dependency that extracts current user if valid Bearer token provided;
    otherwise binds to the isolated X-Guest-Id so guest sessions never share state.
    """
    guest_id = _clean_guest_id(x_guest_id)
    guest_user = {"id": guest_id, "username": "访客", "is_guest": True, "is_admin": False}
    if not authorization:
        return guest_user

    parts = authorization.strip().split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return guest_user

    token = parts[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return guest_user

    user_id = payload["sub"]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, created_at FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return guest_user

    user_data = {
        "id": row["id"],
        "username": row["username"],
        "created_at": row["created_at"],
        "is_guest": False
    }
    user_data["is_admin"] = is_admin_user(user_data)
    return user_data

def get_current_user_required(user: dict = Depends(get_current_user_optional)) -> Dict[str, Any]:
    """Dependency that enforces authentication, returning 401 if missing or invalid."""
    if user.get("is_guest"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="需要登录后方可操作",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

def get_current_admin_user(user: dict = Depends(get_current_user_required)) -> Dict[str, Any]:
    """Dependency that requires valid authentication AND administrator privileges."""
    if not is_admin_user(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，仅管理员可访问后台看板"
        )
    return user
