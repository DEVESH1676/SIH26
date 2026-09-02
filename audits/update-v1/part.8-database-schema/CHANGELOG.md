# Part 8 — Database Schema & SQLAlchemy Models

## Objective
Define the complete new database schema replacing IT-ticket-centric tables with learner-centric schema. Create SQLAlchemy models and Alembic migrations.

## 8.1 Replace `api/models.py` (COMPLETE REWRITE)

```python
"""
Pydantic models for the MoSPI Learning Platform API.
Replaces all IT-ticket-centric models.
"""
from pydantic import BaseModel, Field
from typing import Optional, list
from datetime import datetime


# ── User Models ──────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., max_length=200)
    password: str = Field(..., min_length=8)
    designation: str = Field(..., max_length=200)
    department: str = Field(..., max_length=200)
    role: str = Field(default="learner")


class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    designation: str
    department: str
    roles: list[str]


# ── Course Models ────────────────────────────────────────────

class CourseResponse(BaseModel):
    id: str
    title: str
    description: str
    domain: str
    duration_hours: float
    difficulty: str
    skills: list[str]
    tags: list[str]
    source: str  # "igot" | "local" | "tpac"


class CourseRecommendation(BaseModel):
    courses: list[CourseResponse]
    tpac_programmes: Optional[list[dict]] = []
    estimated_hours: float
    recommended_sequence: list[dict]
    source: str  # "igot" | "fallback"


# ── Competency Models ────────────────────────────────────────

class CompetencyLevel(BaseModel):
    competency_id: str
    competency_name: str
    score: float
    max_score: float = 5.0
    assessed_at: Optional[str] = None
    trend: Optional[str] = None  # "improving" | "stable" | "declining"


class CompetencySummary(BaseModel):
    domain: str
    level: str
    score: float
    strengths: list[str] = []
    gaps: list[str] = []


class CompetencyAnalysis(BaseModel):
    user_id: str
    overall_level: str
    competency_summary: dict[str, CompetencySummary]
    skill_gaps: list[str]
    recommended_pathway: str
    recommended_courses: list[str]
    generated_at: str


# ── Quiz Models ──────────────────────────────────────────────

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: list[str]
    correct_answer: int
    explanation: str
    difficulty: str  # "beginner" | "intermediate" | "advanced"
    category: str


class QuizCreate(BaseModel):
    source_text: str
    num_questions: int = Field(default=10, ge=1, le=50)
    difficulty: str = Field(default="intermediate")
    domain: Optional[str] = None
    source_file: Optional[str] = None


class QuizResponse(BaseModel):
    quiz_id: str
    quiz_title: str
    questions: list[QuizQuestion]
    source: str  # "llm" | "adaptive"


class QuizAttemptRequest(BaseModel):
    quiz_id: str
    answers: dict  # {question_id: selected_option_index}
    time_taken_seconds: int


class QuizResult(BaseModel):
    score: int
    total: int
    percentage: float
    passed: bool
    results: list[dict]


# ── Learning Progress Models ─────────────────────────────────

class LearningSession(BaseModel):
    session_id: str
    activity_type: str
    resource_id: str
    resource_type: str
    duration_seconds: int
    started_at: str
    completed_at: str


class LearningHoursResponse(BaseModel):
    total_sessions: int
    total_hours: float
    average_session_minutes: float
    first_session: Optional[str] = None
    last_session: Optional[str] = None


class CourseProgress(BaseModel):
    course_id: str
    progress: float  # 0-100
    completed_at: Optional[str] = None


# ── Analytics Models ─────────────────────────────────────────

class AdminOverview(BaseModel):
    total_learners: int
    total_learning_sessions: int
    total_quiz_attempts: int
    total_enrolled_courses: int


class WorkforceCompetency(BaseModel):
    competency_id: str
    competency_name: str
    avg_score: float
    assessed_count: int
    mastery_rate: float


class TrainingEffectiveness(BaseModel):
    title: str
    enrolled: int
    avg_score: float
    pass_rate: float


class PredictiveGap(BaseModel):
    competency_id: str
    current_avg: float
    previous_avg: float
    decline_percent: float
    priority: str  # "high" | "medium"


class AdminAnalyticsResponse(BaseModel):
    overview: AdminOverview
    workforce_competency: list[WorkforceCompetency]
    training_effectiveness: list[TrainingEffectiveness]
    predictive_skill_gaps: list[PredictiveGap]


# ── Virtual Assistant Models ─────────────────────────────────

class AssistantRequest(BaseModel):
    message: str
    language: str = Field(default="en")
    user_context: Optional[dict] = None


class AssistantResponse(BaseModel):
    response: str
    suggested_actions: list[dict]
    related_resources: list[dict]
    intent: str


# ── File Upload Models ───────────────────────────────────────

class FileUploadResponse(BaseModel):
    file_id: str
    file_name: str
    file_type: str
    file_size: int
    text_extracted: str
    chunks: list[dict]


class MCQFromFileRequest(BaseModel):
    file_type: str
    num_questions: int = Field(default=10)
    difficulty: str = Field(default="intermediate")
    domain: Optional[str] = None
```

## 8.2 Create `core/database.py` (NEW FILE)

```python
"""
Database initialization — SQLite schema creation and Alembic setup.
"""
import os
import sys
import sqlite3
from pathlib import Path

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
```

## 8.3 Create `alembic/` Directory (if using Alembic for migrations)

```
alembic/
├── env.py
├── script.py.mako
└── versions/
    ├── 001_initial_schema.py
    ├── 002_quiz_tables.py
    ├── 003_learning_sessions.py
    └── 004_audit_log.py
```

## 8.4 Update `main.py` — Initialize Database

```python
from core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    await asyncio.to_thread(init_db)
    print("  ✓ Database initialized")
    
    # ... rest of existing initialization ...
    yield
    # ... cleanup ...
```

## 8.5 Verification Checklist

- [ ] `api/models.py` completely rewritten with learning platform models
- [ ] `core/database.py` creates all tables on startup
- [ ] Default admin user created if not exists
- [ ] `main.py` calls `init_db()` at startup
- [ ] All Pydantic models match the new domain
- [ ] Quiz, attempt, and progress models properly linked
- [ ] Audit log table for compliance
- [ ] File uploads metadata table
- [ ] No remaining IT-ticket references in models
