"""FastAPI middleware — auth, RBAC, rate limiting, CORS."""
import logging
import time

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import get_settings
from core.auth import check_permission, decode_token
from core.security import RateLimiter

settings = get_settings()
rate_limiter = RateLimiter(max_requests=settings.rate_limit_per_minute, window_seconds=60)

def setup_cors(app):
    app.add_middleware(CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"])

async def auth_middleware(request: Request, call_next):
    public_paths = ["/api/health", "/api/auth/login", "/api/auth/register", "/api/auth/refresh", "/docs", "/openapi.json"]
    if request.url.path in public_paths or not request.url.path.startswith("/api/"):
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
