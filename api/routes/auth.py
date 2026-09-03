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
