"""
Learner Progress Store - Captures every learning assessment, quiz attempt, and pathway progress.

Stores competency assessments, quiz scores, and learning pathway progression 
in a local SQLite database (learner_progress.db).
"""
import os
import sys
import json
import sqlite3
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ProgressStore:
    """Persistent SQLite store for tracking learner progress and assessments."""

    def __init__(self, db_path=None):
        if db_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(project_root, "data", "learner_progress.db")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        """Create the LMS tables if they don't exist."""
        # Assessments tracking (Competency Gap Analysis)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS competency_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learner_id TEXT,
                designation TEXT,
                current_skills TEXT,
                skill_gaps TEXT,
                analysis_summary TEXT,
                created_at TIMESTAMP
            )
        """)
        
        # Course / Pathway progress
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learner_id TEXT,
                event_type TEXT,
                course_id TEXT,
                quiz_id TEXT,
                score REAL,
                event_data TEXT,
                created_at TIMESTAMP
            )
        """)
        self.conn.commit()

    def log_assessment(
        self,
        learner_id: str,
        designation: str,
        current_skills: dict,
        skill_gaps: dict,
        analysis_summary: str
    ):
        """Log a competency profile assessment."""
        now = datetime.now(timezone.utc).isoformat()
        
        self.conn.execute(
            """
            INSERT INTO competency_assessments
                (learner_id, designation, current_skills, skill_gaps, analysis_summary, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                learner_id,
                designation,
                json.dumps(current_skills),
                json.dumps(skill_gaps),
                analysis_summary,
                now
            ),
        )
        self.conn.commit()

    def log_event(
        self,
        learner_id: str,
        event_type: str,
        course_id: str = None,
        quiz_id: str = None,
        score: float = None,
        event_data: dict = None
    ):
        """Log a learning event (e.g. course_started, course_completed, quiz_attempt)."""
        now = datetime.now(timezone.utc).isoformat()
        
        self.conn.execute(
            """
            INSERT INTO learning_events
                (learner_id, event_type, course_id, quiz_id, score, event_data, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                learner_id,
                event_type,
                course_id,
                quiz_id,
                score,
                json.dumps(event_data) if event_data else None,
                now
            ),
        )
        self.conn.commit()

    def get_learner_assessments(self, learner_id: str) -> list[dict]:
        """Return all assessments for a learner."""
        cursor = self.conn.execute(
            "SELECT * FROM competency_assessments WHERE learner_id = ? ORDER BY created_at DESC",
            (learner_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        """Close the database connection."""
        self.conn.close()


# --- CLI Self-Test ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Learner Progress Store — Self Test")
    print("=" * 60)

    store = ProgressStore()
    print(f"\n✓ Database created at: {store.db_path}")

    # Insert a test row
    store.log_assessment(
        learner_id="EMP-001",
        designation="Statistical Officer",
        current_skills={"Domain": ["STAT-001"]},
        skill_gaps={"Functional": ["FUNC-002"]},
        analysis_summary="Needs Python training."
    )
    
    store.log_event(
        learner_id="EMP-001",
        event_type="quiz_attempt",
        quiz_id="QZ-101",
        score=85.5,
        event_data={"passed": True}
    )
    print("✓ Test rows inserted successfully")

    rows = store.get_learner_assessments("EMP-001")
    print(f"✓ Total assessments for EMP-001: {len(rows)}")

    store.close()
    print("\n✓ Progress store self-test PASSED")
