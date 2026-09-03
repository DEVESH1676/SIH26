"""
Authentication module — JWT-based auth with RBAC.
"""
import os, sys, datetime
from typing import Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings
from jose import JWTError, jwt
from passlib.context import CryptContext

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

# Run DB initialization when module is imported
init_auth_db()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

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
    # Check user_roles table, and fallback to users.roles
    rows = conn.execute("SELECT role FROM user_roles WHERE user_id = ?", (user_id,)).fetchall()
    if not rows:
        user_row = conn.execute("SELECT roles FROM users WHERE id = ?", (user_id,)).fetchone()
        if user_row and user_row[0]:
            roles = user_row[0].split(",")
            conn.close()
            return roles
    conn.close()
    return [r[0] for r in rows] if rows else ["learner"]

def check_permission(user_id: str, required_permission: str) -> bool:
    roles = get_user_roles(user_id)
    for role in roles:
        if required_permission in ROLES.get(role, {}).get("permissions", []):
            return True
    return False
