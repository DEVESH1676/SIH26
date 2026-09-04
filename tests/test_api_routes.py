"""
Integration tests for FastAPI backend routes.
Tests all HTTP endpoints: health, auth, analyze-profile, pipeline.
Uses httpx TestClient for in-process testing without starting a server.
"""
import os
import sys
import tempfile
import json
import pytest
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def set_test_env():
    """Ensure test environment uses a temporary database."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        os.environ["SQLITE_PATH"] = f.name
    from config.settings import get_settings
    get_settings().sqlite_path = os.environ["SQLITE_PATH"]
    from core.database import init_db
    init_db()
    yield os.environ["SQLITE_PATH"]
    try:
        os.unlink(os.environ["SQLITE_PATH"])
    except FileNotFoundError:
        pass


class TestHealthEndpoint:
    """Test GET /api/health endpoint."""

    def test_health_returns_ok(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert "database" in data

    def test_health_is_json(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.get("/api/health")
        assert "application/json" in resp.headers.get("content-type", "")


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_register_new_user(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)
        resp = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepass123",
            "designation": "Analyst",
            "department": "Testing",
            "role": "learner"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data
        assert "user_id" in data

    def test_register_duplicate_user(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)
        client.post("/api/auth/register", json={
            "username": "dupuser",
            "email": "dup@example.com",
            "password": "securepass123",
            "designation": "Analyst",
            "department": "Testing"
        })
        resp = client.post("/api/auth/register", json={
            "username": "dupuser",
            "email": "dup@example.com",
            "password": "securepass123",
            "designation": "Analyst",
            "department": "Testing"
        })
        assert resp.status_code == 409

    def test_register_duplicate_email(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)
        client.post("/api/auth/register", json={
            "username": "user1",
            "email": "same@example.com",
            "password": "securepass123",
            "designation": "Analyst",
            "department": "Testing"
        })
        resp = client.post("/api/auth/register", json={
            "username": "user2",
            "email": "same@example.com",
            "password": "securepass123",
            "designation": "Analyst",
            "department": "Testing"
        })
        assert resp.status_code == 409

    def test_register_short_username_rejected(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.post("/api/auth/register", json={
            "username": "ab",
            "email": "test@example.com",
            "password": "securepass123",
            "designation": "Analyst",
            "department": "Testing"
        })
        assert resp.status_code == 422

    def test_register_short_password_rejected(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "short",
            "designation": "Analyst",
            "department": "Testing"
        })
        assert resp.status_code == 422

    def test_register_missing_fields_rejected(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.post("/api/auth/register", json={
            "username": "testuser"
        })
        assert resp.status_code == 422

    def test_login_with_registered_user(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)
        client.post("/api/auth/register", json={
            "username": "logintest",
            "email": "login@example.com",
            "password": "securepass123",
            "designation": "Analyst",
            "department": "Testing"
        })
        resp = client.post("/api/auth/login", json={
            "username": "logintest",
            "password": "securepass123"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user_id" in data
        assert "roles" in data

    def test_login_wrong_password(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)
        client.post("/api/auth/register", json={
            "username": "wrongpass",
            "email": "wrong@example.com",
            "password": "correct123",
            "designation": "Analyst",
            "department": "Testing"
        })
        resp = client.post("/api/auth/login", json={
            "username": "wrongpass",
            "password": "wrongpass"
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.post("/api/auth/login", json={
            "username": "nonexistent123",
            "password": "somepassword"
        })
        assert resp.status_code == 401

    def test_get_me_unauthenticated(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_get_me_authenticated(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)
        # Register and login
        client.post("/api/auth/register", json={
            "username": "metest",
            "email": "me@example.com",
            "password": "securepass123",
            "designation": "Tester",
            "department": "QA"
        })
        resp = client.post("/api/auth/login", json={
            "username": "metest",
            "password": "securepass123"
        })
        token = resp.json()["access_token"]

        # Now get /me
        resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        data = resp.json()
        assert "username" in data
        assert "email" in data
        assert "roles" in data
        assert data["username"] == "metest"

    def test_refresh_token_endpoint(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)
        # Register and login
        client.post("/api/auth/register", json={
            "username": "refreshtest",
            "email": "refresh@example.com",
            "password": "securepass123",
            "designation": "Tester",
            "department": "QA"
        })
        resp = client.post("/api/auth/login", json={
            "username": "refreshtest",
            "password": "securepass123"
        })
        refresh_token = resp.json()["refresh_token"]

        # Refresh access token
        resp = client.post("/api/auth/refresh", headers={
            "Authorization": f"Bearer {refresh_token}"
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_refresh_with_access_token_fails(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)
        client.post("/api/auth/register", json={
            "username": "accesstest",
            "email": "accesstest@example.com",
            "password": "securepass123",
            "designation": "Tester",
            "department": "QA"
        })
        resp = client.post("/api/auth/login", json={
            "username": "accesstest",
            "password": "securepass123"
        })
        access_token = resp.json()["access_token"]

        # Try to use access token as refresh token
        resp = client.post("/api/auth/refresh", headers={
            "Authorization": f"Bearer {access_token}"
        })
        assert resp.status_code == 401

    def test_no_auth_header_returns_401(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        resp = client.post("/api/auth/refresh")
        assert resp.status_code == 401


class TestAdminAndAuth:
    """Test admin user setup and admin access."""

    def test_default_admin_exists(self):
        from config.settings import get_settings
        settings = get_settings()
        import sqlite3
        conn = sqlite3.connect(settings.sqlite_path)
        admin = conn.execute(
            "SELECT username, roles FROM users WHERE username = ?", ("admin",)
        ).fetchone()
        conn.close()

        assert admin is not None
        assert admin[0] == "admin"
        assert "admin" in admin[1].split(",")

    def test_default_admin_password_works(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)
        resp = client.post("/api/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_admin_can_access_me(self):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app, follow_redirects=False)
        resp = client.post("/api/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        token = resp.json()["access_token"]
        resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["username"] == "admin"
