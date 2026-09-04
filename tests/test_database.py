"""
Comprehensive tests for database module (core/database.py).
Tests DB initialization, table creation, and default admin user.
"""
import os
import sys
import tempfile
import pytest
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture()
def db_path(shared_db_path):
    """Create a temporary SQLite database. Uses shared_db_path fixture from conftest."""
    return shared_db_path


class TestInitDB:
    """Test database initialization."""

    def test_all_tables_created(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        tables = [row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()]
        conn.close()

        expected_tables = [
            "users", "user_roles", "competency_scores", "quizzes",
            "quiz_questions", "quiz_attempts", "learning_sessions",
            "learner_progress", "audit_log", "file_uploads", "db_metadata"
        ]
        for table in expected_tables:
            assert table in tables, f"Missing table: {table}"

    def test_users_table_schema(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        schema = conn.execute("PRAGMA table_info(users)").fetchall()
        conn.close()

        column_names = [col[1] for col in schema]
        expected_cols = ["id", "username", "email", "password_hash", "designation", "department", "roles", "created_at"]
        for col in expected_cols:
            assert col in column_names, f"Missing column in users: {col}"

    def test_quiz_questions_table_schema(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        schema = conn.execute("PRAGMA table_info(quiz_questions)").fetchall()
        conn.close()

        column_names = [col[1] for col in schema]
        assert "id" in column_names
        assert "quiz_id" in column_names
        assert "question" in column_names
        assert "options" in column_names
        assert "correct_answer" in column_names

    def test_quiz_attempts_table_schema(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        schema = conn.execute("PRAGMA table_info(quiz_attempts)").fetchall()
        conn.close()

        column_names = [col[1] for col in schema]
        assert "attempt_id" in column_names
        assert "quiz_id" in column_names
        assert "learner_id" in column_names
        assert "answers" in column_names
        assert "score" in column_names

    def test_learning_sessions_table_schema(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        schema = conn.execute("PRAGMA table_info(learning_sessions)").fetchall()
        conn.close()

        column_names = [col[1] for col in schema]
        assert "session_id" in column_names
        assert "learner_id" in column_names
        assert "activity_type" in column_names

    def test_audit_log_table_schema(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        schema = conn.execute("PRAGMA table_info(audit_log)").fetchall()
        conn.close()

        column_names = [col[1] for col in schema]
        assert "id" in column_names
        assert "action" in column_names
        assert "user_id" in column_names


class TestDefaultAdminUser:
    """Test that default admin user is created on init."""

    def test_admin_user_created(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        admin = conn.execute(
            "SELECT id, username, email, designation, roles FROM users WHERE username = ?",
            ("admin",)
        ).fetchone()
        conn.close()

        assert admin is not None
        assert admin[1] == "admin"
        assert admin[2] == "admin@mospi.gov.in"
        assert admin[3] == "System Administrator"
        assert "admin" in admin[4]

    def test_admin_password_is_hashed(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        pw_hash = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?", ("admin",)
        ).fetchone()[0]
        conn.close()

        assert pw_hash.startswith("$2b$")

    def test_admin_password_works(self, db_path):
        from core.database import init_db
        from core.auth import verify_password
        init_db()

        conn = sqlite3.connect(db_path)
        pw_hash = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?", ("admin",)
        ).fetchone()[0]
        conn.close()

        assert verify_password("admin123", pw_hash) is True

    def test_admin_not_created_twice(self, db_path):
        from core.database import init_db
        init_db()
        init_db()  # Call twice

        conn = sqlite3.connect(db_path)
        admins = conn.execute(
            "SELECT COUNT(*) FROM users WHERE username = ?", ("admin",)
        ).fetchone()[0]
        conn.close()

        assert admins == 1

    def test_custom_user_can_be_registered(self, db_path):
        from core.database import init_db
        from core.auth import hash_password
        init_db()

        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT INTO users (id, username, email, password_hash, designation, department, roles) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("test-1", "testuser", "test@example.com", hash_password("pass123"), "Analyst", "Stats", "learner")
        )
        conn.commit()
        conn.close()

        conn = sqlite3.connect(db_path)
        user = conn.execute(
            "SELECT username, email FROM users WHERE username = ?", ("testuser",)
        ).fetchone()
        conn.close()

        assert user is not None
        assert user[0] == "testuser"


class TestTablesForDataOperations:
    """Test that tables support expected data operations."""

    def test_insert_and_select_learner_progress(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT INTO learner_progress (learner_id, course_id, progress_percent, last_accessed) VALUES (?, ?, ?, ?)",
            ("l1", "c1", 50.0, "2025-01-01T00:00:00")
        )
        conn.commit()
        row = conn.execute(
            "SELECT progress_percent FROM learner_progress WHERE learner_id = ?", ("l1",)
        ).fetchone()
        conn.close()

        assert row is not None
        assert row[0] == 50.0

    def test_insert_and_select_competency_scores(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT INTO competency_scores (learner_id, competency_id, score, assessment_type) VALUES (?, ?, ?, ?)",
            ("l1", "STAT-001", 4.5, "quiz")
        )
        conn.commit()
        row = conn.execute(
            "SELECT score FROM competency_scores WHERE learner_id = ? AND competency_id = ?",
            ("l1", "STAT-001")
        ).fetchone()
        conn.close()

        assert row is not None
        assert row[0] == 4.5

    def test_file_uploads_table(self, db_path):
        from core.database import init_db
        init_db()

        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT INTO file_uploads (file_id, user_id, filename, file_type, file_size) VALUES (?, ?, ?, ?, ?)",
            ("f1", "u1", "test.pdf", "pdf", 1024)
        )
        conn.commit()
        row = conn.execute(
            "SELECT filename, file_type FROM file_uploads WHERE file_id = ?", ("f1",)
        ).fetchone()
        conn.close()

        assert row is not None
        assert row[0] == "test.pdf"
