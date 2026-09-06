"""
Learning Hours & Progress Tracker.
Tracks total learning time, course progress, and activity logs.
"""
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings

settings = get_settings()


class LearningTracker:
    """Track learning hours, progress, and activity for each learner."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or settings.sqlite_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS learner_progress (
                learner_id TEXT,
                course_id TEXT,
                progress_percent REAL DEFAULT 0,
                last_accessed TIMESTAMP,
                completed_at TIMESTAMP,
                PRIMARY KEY (learner_id, course_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS competency_scores (
                learner_id TEXT,
                competency_id TEXT,
                score REAL,
                assessed_at TIMESTAMP,
                assessment_type TEXT,
                PRIMARY KEY (learner_id, competency_id)
            )
        """)
        conn.commit()
        conn.close()

    def log_activity(
        self,
        learner_id: str,
        activity_type: str,
        resource_id: str | None = None,
        resource_type: str | None = None,
        duration_seconds: int = 0,
        metadata: dict | None = None,
    ) -> str:
        """Log a learning activity session."""
        import uuid
        session_id = str(uuid.uuid4())[:8]
        now = datetime.now(timezone.utc).isoformat()

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """INSERT INTO learning_sessions 
               (session_id, learner_id, activity_type, resource_id, resource_type,
                duration_seconds, started_at, completed_at, metadata)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (session_id, learner_id, activity_type, resource_id, resource_type,
             duration_seconds, now, now, json.dumps(metadata or {})),
        )
        conn.commit()
        conn.close()
        return session_id

    def get_learning_hours(self, learner_id: str, period_days: int = 30) -> dict:
        """Get total learning hours for a learner over a period."""
        conn = sqlite3.connect(self.db_path)
        cutoff = (datetime.now(timezone.utc) - timedelta(days=period_days)).isoformat()

        stats = conn.execute(
            """SELECT 
                  COUNT(*) as total_sessions,
                  SUM(duration_seconds) as total_seconds,
                  AVG(duration_seconds) as avg_duration,
                  MIN(started_at) as first_session,
                  MAX(started_at) as last_session
               FROM learning_sessions 
               WHERE learner_id = ? AND started_at >= ?""",
            (learner_id, cutoff),
        ).fetchone()
        conn.close()

        return {
            "total_sessions": stats[0] or 0,
            "total_hours": round((stats[1] or 0) / 3600, 2),
            "average_session_minutes": round((stats[2] or 0) / 60, 1),
            "first_session": stats[3],
            "last_session": stats[4],
        }

    def update_course_progress(
        self,
        learner_id: str,
        course_id: str,
        progress_percent: float,
    ):
        """Update a learner's progress in a course."""
        now = datetime.now(timezone.utc).isoformat()
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """INSERT OR REPLACE INTO learner_progress 
               (learner_id, course_id, progress_percent, last_accessed)
               VALUES (?, ?, ?, ?)""",
            (learner_id, course_id, progress_percent, now),
        )
        if progress_percent >= 100:
            conn.execute(
                "UPDATE learner_progress SET completed_at = ? WHERE learner_id = ? AND course_id = ?",
                (now, learner_id, course_id),
            )
        conn.commit()
        conn.close()

    def get_learner_dashboard_data(self, learner_id: str) -> dict:
        """Get all dashboard data for a learner in one query."""
        conn = sqlite3.connect(self.db_path)

        # Learning hours
        hours = self.get_learning_hours(learner_id)

        # Course progress
        courses = conn.execute(
            """SELECT course_id, progress_percent, completed_at 
               FROM learner_progress 
               WHERE learner_id = ?""",
            (learner_id,),
        ).fetchall()

        # Competency scores
        competencies = conn.execute(
            "SELECT competency_id, score, assessed_at FROM competency_scores WHERE learner_id = ?",
            (learner_id,),
        ).fetchall()

        conn.close()

        return {
            "learning_hours": hours,
            "course_progress": [
                {"course_id": c[0], "progress": c[1], "completed_at": c[2]}
                for c in courses
            ],
            "competency_scores": [
                {"competency_id": c[0], "score": c[1], "assessed_at": c[2]}
                for c in competencies
            ],
        }
