import os
import time
import secrets
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, status
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

def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Dependency that extracts current user if valid Bearer token provided;
    otherwise falls back to a safe guest default user so non-logged-in users can still practice.
    """
    guest_user = {"id": "default", "username": "访客", "is_guest": True}
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

    return {
        "id": row["id"],
        "username": row["username"],
        "created_at": row["created_at"],
        "is_guest": False
    }

def get_current_user_required(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Dependency that enforces authentication, returning 401 if missing or invalid."""
    user = get_current_user_optional(authorization)
    if user.get("is_guest"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="需要登录后方可操作",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
