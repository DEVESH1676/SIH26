"""
Database initialization — SQLite schema creation and Alembic setup.
"""
import os
import sqlite3
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings

settings = get_settings()


def init_db():
    """Create all database tables."""
    os.makedirs(os.path.dirname(settings.sqlite_path), exist_ok=True)
    conn = sqlite3.connect(settings.sqlite_path)

    # Users
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            designation TEXT,
            department TEXT,
            roles TEXT DEFAULT 'learner',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # User roles (for multi-role support)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Competency assessments
    conn.execute("""
        CREATE TABLE IF NOT EXISTS competency_scores (
            learner_id TEXT NOT NULL,
            competency_id TEXT NOT NULL,
            score REAL NOT NULL,
            assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            assessment_type TEXT,
            PRIMARY KEY (learner_id, competency_id)
        )
    """)

    # Quizzes
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            quiz_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            source_file TEXT,
            source_text TEXT,
            difficulty TEXT,
            num_questions INTEGER,
            domain TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Quiz questions
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id TEXT NOT NULL,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            difficulty TEXT,
            category TEXT,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
        )
    """)

    # Quiz attempts
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            attempt_id TEXT PRIMARY KEY,
            quiz_id TEXT NOT NULL,
            learner_id TEXT NOT NULL,
            answers TEXT NOT NULL,
            score REAL,
            total_questions INTEGER,
            time_taken_seconds INTEGER,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
        )
    """)

    # Learning sessions
    conn.execute("""
        CREATE TABLE IF NOT EXISTS learning_sessions (
            session_id TEXT PRIMARY KEY,
            learner_id TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            resource_id TEXT,
            resource_type TEXT,
            duration_seconds INTEGER,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            metadata TEXT
        )
    """)

    # Learner course progress
    conn.execute("""
        CREATE TABLE IF NOT EXISTS learner_progress (
            learner_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            progress_percent REAL DEFAULT 0,
            last_accessed TIMESTAMP,
            completed_at TIMESTAMP,
            PRIMARY KEY (learner_id, course_id)
        )
    """)

    # Audit log
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            user_id TEXT,
            resource TEXT,
            details TEXT,
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # File uploads metadata
    conn.execute("""
        CREATE TABLE IF NOT EXISTS file_uploads (
            file_id TEXT PRIMARY KEY,
            user_id TEXT,
            filename TEXT,
            file_type TEXT,
            file_size INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )
    """)

    # ChromaDB collection name (stored for reference)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS db_metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # Default admin user (if not exists)
    from core.auth import hash_password
    admin_exists = conn.execute("SELECT 1 FROM users WHERE username = ?", ("admin",)).fetchone()
    if not admin_exists:
        import uuid
        admin_id = str(uuid.uuid4())[:8]
        conn.execute(
            "INSERT INTO users (id, username, email, password_hash, designation, roles) VALUES (?, ?, ?, ?, ?, ?)",
            (admin_id, "admin", "admin@mospi.gov.in", hash_password("admin123"),
             "System Administrator", "admin"))

    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")
