# Part 7 — Authentication, Security & RBAC

## Objective
Implement complete authentication system with JWT, role-based access control, input sanitization, and security middleware.

## 7.1 Create `core/auth.py` (NEW FILE)

```python
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
    rows = conn.execute("SELECT role FROM user_roles WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return [r[0] for r in rows] if rows else ["learner"]

def check_permission(user_id: str, required_permission: str) -> bool:
    roles = get_user_roles(user_id)
    for role in roles:
        if required_permission in ROLES.get(role, {}).get("permissions", []):
            return True
    return False
```

## 7.2 Create `core/security.py` (NEW FILE)

```python
"""Security utilities — sanitization, rate limiting, audit logging."""
import re, time, logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)
    def is_allowed(self, key: str) -> bool:
        now = time.time()
        self.requests[key] = [t for t in self.requests[key] if now - t < self.window]
        if len(self.requests[key]) >= self.max_requests:
            return False
        self.requests[key].append(now)
        return True

def sanitize_llm_input(text: str, max_length: int = 50000) -> str:
    if not text:
        return ""
    text = text[:max_length]
    text = re.sub(r'(?i)(system:|you are|ignore previous|prompt:)', '', text)
    text = text.replace('```', '')
    return text.strip()

def audit_log(action: str, user_id: str, resource: str = None, details: dict = None):
    import sqlite3, json
    from datetime import datetime, timezone
    conn = sqlite3.connect(settings.sqlite_path)
    conn.execute(
        "INSERT INTO audit_log (action, user_id, resource, details, logged_at) VALUES (?, ?, ?, ?, ?)",
        (action, user_id, resource, json.dumps(details or {}), datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()
    logger.info(f"AUDIT: {action} by {user_id} on {resource}")
```

## 7.3 Create `api/middleware.py` (NEW FILE)

```python
"""FastAPI middleware — auth, RBAC, rate limiting, CORS."""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time, logging

from core.auth import decode_token, check_permission
from core.security import RateLimiter
from config.settings import get_settings

settings = get_settings()
rate_limiter = RateLimiter(max_requests=settings.rate_limit_per_minute, window_seconds=60)

def setup_cors(app):
    app.add_middleware(CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"])

async def auth_middleware(request: Request, call_next):
    public_paths = ["/api/health", "/api/auth/login", "/api/auth/refresh", "/docs", "/openapi.json"]
    if request.url.path in public_paths or request.url.path.startswith("/static"):
        return await call_next(request)
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "No authentication token"})
    payload = decode_token(auth_header.split(" ", 1)[1])
    if not payload:
        return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})
    request.state.user_id = payload.get("sub")
    request.state.roles = payload.get("roles", ["learner"])
    return await call_next(request)

async def rbac_middleware(request: Request, call_next):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        return await call_next(request)
    admin_paths = ["/api/admin/", "/api/analytics/admin/"]
    for path in admin_paths:
        if request.url.path.startswith(path):
            if not check_permission(user_id, "view_analytics"):
                return JSONResponse(status_code=403, content={"detail": "Insufficient permissions"})
    return await call_next(request)

async def rate_limit_middleware(request: Request, call_next):
    if not rate_limiter.is_allowed(request.client.host):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
    return await call_next(request)

async def audit_logging_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    user_id = getattr(request.state, "user_id", "anonymous")
    logging.info(f"REQUEST: {request.method} {request.url.path} → {response.status_code} ({duration:.3f}s) by {user_id}")
    return response
```

## 7.4 Create `api/routes/auth.py` (NEW FILE)

```python
"""Authentication routes — login, register, refresh, logout."""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
import sqlite3, uuid
from core.auth import (hash_password, verify_password, create_access_token,
                       create_refresh_token, decode_token, get_user_roles, check_permission)
from config.settings import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/auth", tags=["authentication"])

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., max_length=200)
    password: str = Field(..., min_length=8)
    designation: str = Field(..., max_length=200)
    department: str = Field(..., max_length=200)
    role: str = Field(default="learner")

@router.post("/login")
async def login(req: LoginRequest):
    conn = sqlite3.connect(settings.sqlite_path)
    user = conn.execute(
        "SELECT id, username, password_hash, roles FROM users WHERE username = ?", (req.username,)).fetchone()
    conn.close()
    if not user or not verify_password(req.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id, username = str(user[0]), user[1]
    roles = user[3].split(",") if user[3] else ["learner"]
    return {
        "access_token": create_access_token({"sub": user_id, "roles": roles}),
        "refresh_token": create_refresh_token({"sub": user_id, "roles": roles}),
        "token_type": "bearer",
        "user_id": user_id,
        "roles": roles,
    }

@router.post("/register")
async def register(req: RegisterRequest):
    conn = sqlite3.connect(settings.sqlite_path)
    existing = conn.execute(
        "SELECT id FROM users WHERE username = ? OR email = ?", (req.username, req.email)).fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=409, detail="Username or email already exists")
    user_id = str(uuid.uuid4())[:8]
    conn.execute(
        "INSERT INTO users (id, username, email, password_hash, designation, department, roles) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, req.username, req.email, hash_password(req.password), req.designation, req.department, req.role))
    conn.commit()
    conn.close()
    return {"message": "User registered", "user_id": user_id}

@router.post("/refresh")
async def refresh(request: Request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No refresh token")
    payload = decode_token(auth_header.split(" ", 1)[1])
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return {"access_token": create_access_token({"sub": payload["sub"], "roles": payload.get("roles", [])})}

@router.get("/me")
async def get_me(request: Request):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    conn = sqlite3.connect(settings.sqlite_path)
    user = conn.execute(
        "SELECT id, username, email, designation, department, roles FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user[0], "username": user[1], "email": user[2], "designation": user[3],
            "department": user[4], "roles": user[5].split(",") if user[5] else ["learner"]}
```

## 7.5 Update `main.py` — Add Auth Middleware & Routes

```python
from api.middleware import setup_cors, auth_middleware, rbac_middleware, rate_limit_middleware, audit_logging_middleware
from api.routes import auth as auth_routes

# In lifespan:
setup_cors(app)
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(auth_middleware)
app.middleware("http")(rbac_middleware)
app.middleware("http")(audit_logging_middleware)

# Register auth routes
app.include_router(auth_routes.router)
```

## 7.6 Update `requirements.txt`

```
# Add to existing requirements.txt:
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.9
```

## 7.7 Verification Checklist

- [ ] `core/auth.py` — JWT creation, decoding, password hashing
- [ ] `core/security.py` — Rate limiting, sanitization, audit logging
- [ ] `api/middleware.py` — Auth, RBAC, rate limit, CORS, audit middleware
- [ ] `api/routes/auth.py` — Login, register, refresh, logout, profile endpoints
- [ ] `main.py` registers middleware and auth routes
- [ ] `requirements.txt` updated with `python-jose`, `passlib`, `python-multipart`
- [ ] SQLite `users`, `user_roles`, `audit_log` tables created
- [ ] Admin-only endpoints protected
- [ ] Rate limiting configurable via settings
- [ ] Prompt injection sanitization active
