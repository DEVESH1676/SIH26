"""
Quiz attempt tracker — records and analyzes learner quiz attempts.
"""
import os
import sys
import json
import uuid
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings

settings = get_settings()


class AttemptTracker:
    """Track and analyze quiz attempt history for learners."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.sqlite_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def record_attempt(
        self,
        quiz_id: str,
        learner_id: str,
        answers: dict,
        score: float,
        total: int,
        time_taken_seconds: int,
    ) -> str:
        """Record a quiz attempt."""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        attempt_id = str(uuid.uuid4())[:8]
        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            """INSERT INTO quiz_attempts 
               (attempt_id, quiz_id, learner_id, answers, score, total_questions, 
                time_taken_seconds, started_at, completed_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (attempt_id, quiz_id, learner_id, json.dumps(answers),
             score, total, time_taken_seconds, now, now),
        )
        conn.commit()
        conn.close()
        return attempt_id

    def get_learner_history(self, learner_id: str, limit: int = 20) -> list[dict]:
        """Get quiz attempt history for a learner."""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            """SELECT qa.*, q.title as quiz_title, q.difficulty as quiz_difficulty
               FROM quiz_attempts qa
               LEFT JOIN quizzes q ON qa.quiz_id = q.quiz_id
               WHERE qa.learner_id = ?
               ORDER BY qa.completed_at DESC
               LIMIT ?""",
            (learner_id, limit),
        ).fetchall()
        conn.close()

        results = []
        for row in rows:
            results.append({
                "attempt_id": row[0],
                "quiz_id": row[1],
                "quiz_title": row[9],
                "quiz_difficulty": row[10],
                "score": row[4],
                "total": row[5],
                "percentage": round((row[4] / row[5] * 100) if row[5] > 0 else 0, 1),
                "time_taken": row[6],
                "completed_at": row[8],
            })
        return results

    def get_learner_performance(self, learner_id: str) -> dict:
        """Get aggregated performance metrics for a learner."""
        import sqlite3
        conn = sqlite3.connect(self.db_path)

        stats = conn.execute(
            """SELECT 
                  COUNT(*) as total_attempts,
                  AVG(CAST(score AS REAL) / total_questions * 100) as avg_score,
                  MAX(CAST(score AS REAL) / total_questions * 100) as best_score,
                  MIN(CAST(score AS REAL) / total_questions * 100) as worst_score,
                  AVG(time_taken_seconds) as avg_time_seconds,
                  SUM(CASE WHEN CAST(score AS REAL) / total_questions >= 0.6 THEN 1 ELSE 0 END) as passed_count
               FROM quiz_attempts 
               WHERE learner_id = ?""",
            (learner_id,),
        ).fetchone()
        conn.close()

        return {
            "total_attempts": stats[0] or 0,
            "average_score": round(stats[1] or 0, 1),
            "best_score": round(stats[2] or 0, 1),
            "worst_score": round(stats[3] or 0, 1),
            "average_time_seconds": round(stats[4] or 0, 1),
            "passed_count": stats[5] or 0,
            "pass_rate": round(
                ((stats[5] or 0) / (stats[0] or 1)) * 100, 1
            ),
        }
