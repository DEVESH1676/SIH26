"""
Authentication module — JWT-based auth with RBAC.
"""
import os, sys, datetime
from typing import Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings
from jose import JWTError, jwt
import bcrypt

settings = get_settings()

ROLES = {
    "admin":   {"permissions": ["read", "write", "delete", "manage_users", "view_analytics"]},
    "trainer": {"permissions": ["read", "write", "view_analytics"]},
    "learner": {"permissions": ["read", "write_own"]},
    "viewer":  {"permissions": ["read"]},
}

def init_auth_db():
    import sqlite3
    conn = sqlite3.connect(settings.sqlite_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            designation TEXT,
            department TEXT,
            roles TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id TEXT,
            role TEXT,
            PRIMARY KEY (user_id, role)
        )
    """)
    conn.commit()
    conn.close()

# NOTE: DB initialization is handled by core/database.init_db()
# to avoid duplicate table creation and import-order issues.

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + (
        expires_delta or datetime.timedelta(minutes=settings.jwt_access_token_expiry_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def create_refresh_token(data: dict) -> str:
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=settings.jwt_refresh_token_expiry_days
    )
    data["iat"] = datetime.datetime.now(datetime.timezone.utc)
    data["exp"] = expire
    data["type"] = "refresh"
    return jwt.encode(data, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None

def get_user_roles(user_id: str) -> list[str]:
    import sqlite3
    conn = sqlite3.connect(settings.sqlite_path)
    try:
        # Check user_roles table, and fallback to users.roles
        rows = conn.execute("SELECT role FROM user_roles WHERE user_id = ?", (user_id,)).fetchall()
        if rows:
            conn.close()
            return [r[0] for r in rows]
        user_row = conn.execute("SELECT roles FROM users WHERE id = ?", (user_id,)).fetchone()
        if user_row and user_row[0]:
            roles = user_row[0].split(",")
            conn.close()
            return roles
    except sqlite3.OperationalError:
        pass  # Tables may not exist yet
    finally:
        conn.close()
    return ["learner"]

def check_permission(user_id: str, required_permission: str) -> bool:
    roles = get_user_roles(user_id)
    for role in roles:
        if required_permission in ROLES.get(role, {}).get("permissions", []):
            return True
    return False

def require_role(role: str):
    """Decorator that enforces a specific role is present on the request."""
    from fastapi import HTTPException

    def decorator(func):
        from functools import wraps
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from kwargs or args
            request = kwargs.get("request") or (
                args[0] if args and hasattr(args[0], "state") else None
            )
            if request is None:
                return await func(*args, **kwargs)
            user_id = getattr(request.state, "user_id", None)
            if not user_id:
                raise HTTPException(status_code=401, detail="Not authenticated")
            user_roles = get_user_roles(user_id)
            if role not in user_roles:
                raise HTTPException(status_code=403, detail=f"Role '{role}' required")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
