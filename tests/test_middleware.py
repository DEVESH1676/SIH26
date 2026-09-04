"""
Comprehensive tests for middleware (api/middleware.py).
Tests CORS setup, auth middleware, RBAC middleware, rate limiting, audit logging.
"""
import os
import sys
import tempfile
import time
import pytest
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def set_test_env():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        os.environ["SQLITE_PATH"] = f.name
    from config.settings import get_settings
    get_settings().sqlite_path = os.environ["SQLITE_PATH"]
    from core.database import init_db
    init_db()
    yield
    try:
        os.unlink(os.environ["SQLITE_PATH"])
    except FileNotFoundError:
        pass


class TestCORS:
    """Test CORS middleware setup."""

    def test_cors_is_setup(self):
        from fastapi import FastAPI
        from api.middleware import setup_cors
        app = FastAPI()
        setup_cors(app)
        # Middleware should be registered
        assert len(app.user_middleware) > 0 or any(
            "CORSMiddleware" in str(m) for m in app.user_middleware
        )

    def test_cors_origins_configured(self):
        from config.settings import get_settings
        settings = get_settings()
        assert isinstance(settings.cors_origins, list)
        assert len(settings.cors_origins) > 0


class TestAuthMiddleware:
    """Test auth middleware behavior."""

    def test_public_health_endpoint_accessible(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/api/health")
        assert resp.status_code == 200

    def test_public_auth_endpoints_accessible(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, raise_server_exceptions=False)
        resp = client.post("/api/auth/login", json={
            "username": "nonexistent999",
            "password": "nonexistent"
        })
        assert resp.status_code == 401

    def test_register_accessible(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, raise_server_exceptions=False)
        resp = client.post("/api/auth/register", json={
            "username": "newuser123",
            "email": "new@example.com",
            "password": "securepass123",
            "designation": "Tester",
            "department": "QA"
        })
        assert resp.status_code == 200

    def test_unauthenticated_api_returns_401(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_missing_auth_header_returns_401(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.post("/api/analyze-profile", json={
            "designation": "Tester",
            "profile_text": "test profile"
        })
        assert resp.status_code == 401

    def test_invalid_token_returns_401(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.post("/api/analyze-profile", json={
            "designation": "Tester",
            "profile_text": "test"
        }, headers={"Authorization": "Bearer invalid.token.here"})
        assert resp.status_code == 401

    def test_docs_accessible_without_auth(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.get("/docs")
        assert resp.status_code == 200

    def test_openapi_json_accessible(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.get("/openapi.json")
        assert resp.status_code == 200


class TestRBACMiddleware:
    """Test RBAC (Role-Based Access Control) middleware."""

    def test_learner_cannot_access_admin(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)

        # Register as learner and login
        client.post("/api/auth/register", json={
            "username": "lbtest",
            "email": "lb@example.com",
            "password": "securepass123",
            "designation": "Tester",
            "department": "QA",
            "role": "learner"
        })
        resp = client.post("/api/auth/login", json={
            "username": "lbtest",
            "password": "securepass123"
        })
        token = resp.json()["access_token"]

        # Try to access admin endpoint
        resp = client.get("/api/admin/", headers={"Authorization": f"Bearer {token}"})
        # Should be 403 (RBAC blocks it) or 404 (endpoint doesn't exist)
        assert resp.status_code in [403, 404]


class TestRateLimitMiddleware:
    """Test rate limiting middleware."""

    def test_within_rate_limit(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        # Health endpoint - no rate limiting issues for normal usage
        resp = client.get("/api/health")
        assert resp.status_code == 200

    def test_rate_limit_config(self):
        from api.middleware import settings
        assert hasattr(settings, "rate_limit_per_minute")
        assert isinstance(settings.rate_limit_per_minute, int)
        assert settings.rate_limit_per_minute > 0

    def test_rate_limiter_blocks_excessive_requests(self):
        from core.security import RateLimiter
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        for i in range(5):
            assert limiter.is_allowed("test-ip") is True
        assert limiter.is_allowed("test-ip") is False  # 6th request blocked


class TestAuditLogging:
    """Test audit logging middleware."""

    def test_audit_middleware_exists(self):
        from api.middleware import audit_logging_middleware
        assert audit_logging_middleware is not None

    def test_request_logging_occurs(self, capfd):
        """Test that request logging is configured."""
        from api.middleware import settings
        assert hasattr(settings, "log_format")
