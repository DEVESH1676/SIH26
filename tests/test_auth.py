"""Comprehensive tests for authentication module (core/auth.py)."""
import sys, os, tempfile, pytest, datetime, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jose import jwt


class TestPasswordHashing:
    """Test hash_password and verify_password."""

    def test_hash_format(self):
        from core.auth import hash_password
        h = hash_password("testpass123")
        assert h.startswith("$2b$")
        assert len(h) > 20

    def test_hash_different_salt(self):
        from core.auth import hash_password
        assert hash_password("same") != hash_password("same")

    def test_verify_correct(self):
        from core.auth import hash_password, verify_password
        pw = "SecurePass!23"
        assert verify_password(pw, hash_password(pw)) is True

    def test_verify_wrong(self):
        from core.auth import hash_password, verify_password
        h = hash_password("correct_pass")
        assert verify_password("wrong_pass", h) is False

    def test_verify_empty(self):
        from core.auth import hash_password, verify_password
        assert verify_password("", hash_password("real")) is False

    def test_verify_unicode(self):
        from core.auth import hash_password, verify_password
        pw = "pässwörd_123_🔒"
        assert verify_password(pw, hash_password(pw)) is True

    def test_verify_none_input(self):
        from core.auth import verify_password
        assert verify_password("", "not_a_hash") is False


class TestJWTTokens:
    """Test JWT creation, decoding, expiry."""

    def test_access_token_valid(self):
        from core.auth import create_access_token
        t = create_access_token({"sub": "user1", "roles": ["admin"]})
        assert isinstance(t, str)
        assert len(t.split(".")) == 3

    def test_access_token_contains_subject(self):
        from core.auth import create_access_token, decode_token
        t = create_access_token({"sub": "user-abc", "roles": ["learner"]})
        d = decode_token(t)
        assert d["sub"] == "user-abc"
        assert "learner" in d["roles"]

    def test_access_token_has_expiry(self):
        from core.auth import create_access_token, decode_token
        t = create_access_token({"sub": "user1"})
        d = decode_token(t)
        assert "exp" in d

    def test_access_token_custom_expiry(self):
        from core.auth import create_access_token, decode_token
        t = create_access_token({"sub": "user1"}, datetime.timedelta(minutes=5))
        d = decode_token(t)
        assert d["exp"] - d.get("iat", d["exp"]) <= 3600

    def test_refresh_token(self):
        from core.auth import create_refresh_token, decode_token
        t = create_refresh_token({"sub": "user1", "roles": ["admin"]})
        d = decode_token(t)
        assert d["type"] == "refresh"
        assert d["sub"] == "user1"

    def test_refresh_token_longer_expiry(self):
        from core.auth import create_refresh_token, decode_token
        t = create_refresh_token({"sub": "user1"})
        d = decode_token(t)
        assert d["exp"] - d.get("iat", d["exp"]) > 500000

    def test_decode_invalid_token(self):
        from core.auth import decode_token
        assert decode_token("invalid.token.here") is None
        assert decode_token("not-a-jwt") is None

    def test_decode_tampered(self):
        from core.auth import create_access_token, decode_token
        t = create_access_token({"sub": "user1"})
        parts = t.split(".")
        tampered = parts[0] + ".fake.payload." + parts[2]
        assert decode_token(tampered) is None

    def test_different_sub_different_tokens(self):
        from core.auth import create_access_token
        assert create_access_token({"sub": "a"}) != create_access_token({"sub": "b"})


class TestRBAC:
    """Test role-based access control."""

    def test_role_definitions(self):
        from core.auth import ROLES
        assert set(ROLES.keys()) == {"admin", "trainer", "learner", "viewer"}

    def test_admin_permissions(self):
        from core.auth import ROLES
        perms = ROLES["admin"]["permissions"]
        assert {"read", "write", "delete", "manage_users", "view_analytics"}.issubset(perms)

    def test_learner_limited_permissions(self):
        from core.auth import ROLES
        perms = ROLES["learner"]["permissions"]
        assert {"read", "write_own"}.issubset(perms)
        assert "delete" not in perms
        assert "manage_users" not in perms
        assert "view_analytics" not in perms

    def test_check_permission(self):
        from core.auth import check_permission
        # Without DB, defaults to ["learner"], no view_analytics
        assert check_permission("any-id", "view_analytics") is False
        assert check_permission("any-id", "read") is True

    def test_require_role_decorator(self):
        from core.auth import require_role
        decorator = require_role("admin")
        assert callable(decorator)
        @decorator
        async def dummy():
            return "ok"
        assert callable(dummy)
