"""
Admin Analytics Engine — Organization-wide insights, workforce analytics,
predictive skill needs, and training effectiveness.
"""
import os
import sys
import sqlite3
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings

settings = get_settings()


class LearningAnalytics:
    """Organization-wide learning analytics for administrators."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.sqlite_path

    def get_admin_overview(self) -> dict:
        """Get high-level admin dashboard overview."""
        conn = sqlite3.connect(self.db_path)

        total_learners = conn.execute("SELECT COUNT(DISTINCT learner_id) FROM learning_sessions").fetchone()[0]
        total_sessions = conn.execute("SELECT COUNT(*) FROM learning_sessions").fetchone()[0]
        total_quizzes = conn.execute("SELECT COUNT(*) FROM quiz_attempts").fetchone()[0]
        total_courses = conn.execute("SELECT COUNT(DISTINCT course_id) FROM learner_progress").fetchone()[0]

        conn.close()

        return {
            "total_learners": total_learners or 0,
            "total_learning_sessions": total_sessions or 0,
            "total_quiz_attempts": total_quizzes or 0,
            "total_enrolled_courses": total_courses or 0,
            "period": "all_time",
        }

    def get_workforce_competency_distribution(self) -> dict:
        """Get competency level distribution across the organization."""
        conn = sqlite3.connect(self.db_path)

        # Get competency scores grouped by competency
        rows = conn.execute(
            """SELECT competency_id, AVG(score) as avg_score, COUNT(*) as count
               FROM competency_scores
               GROUP BY competency_id
               ORDER BY avg_score DESC"""
        ).fetchall()
        conn.close()

        return {
            "competencies": [
                {
                    "competency_id": r[0],
                    "avg_score": round(r[1], 2),
                    "assessed_count": r[2],
                    "mastery_rate": round((r[1] / 5.0) * 100, 1) if r[1] else 0,
                }
                for r in rows
            ]
        }

    def get_training_effectiveness(self, course_id: str = None) -> dict:
        """Calculate training effectiveness metrics."""
        conn = sqlite3.connect(self.db_path)

        if course_id:
            rows = conn.execute(
                """SELECT q.title, COUNT(DISTINCT qa.learner_id) as enrolled,
                          AVG(CAST(qa.score AS REAL) / qa.total_questions * 100),
                          SUM(CASE WHEN CAST(qa.score AS REAL) / qa.total_questions >= 0.6 THEN 1 ELSE 0 END)
                   FROM quizzes q
                   LEFT JOIN quiz_attempts qa ON q.quiz_id = qa.quiz_id
                   WHERE q.quiz_id IN (
                       SELECT quiz_id FROM quiz_questions
                       WHERE category LIKE '%' || ? || '%'
                   )
                   GROUP BY q.quiz_id
                   ORDER BY enrolled DESC""",
                (course_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT q.title, COUNT(DISTINCT qa.learner_id) as enrolled,
                          AVG(CAST(qa.score AS REAL) / qa.total_questions * 100),
                          SUM(CASE WHEN CAST(qa.score AS REAL) / qa.total_questions >= 0.6 THEN 1 ELSE 0 END)
                   FROM quizzes q
                   LEFT JOIN quiz_attempts qa ON q.quiz_id = qa.quiz_id
                   GROUP BY q.quiz_id
                   ORDER BY enrolled DESC"""
            ).fetchall()
        conn.close()

        return {
            "courses": [
                {
                    "title": r[0],
                    "enrolled": r[1] or 0,
                    "avg_score": round(r[2] or 0, 1),
                    "pass_rate": round(((r[3] or 0) / (r[1] or 1)) * 100, 1),
                }
                for r in rows
            ]
        }

    def get_predictive_skill_needs(self) -> dict:
        """
        Predictive analytics — identify emerging skill gaps based on:
        1. Trending competency score decreases
        2. New job role requirements
        3. Industry trends
        """
        # Simple heuristic: competencies with decreasing average scores
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            """SELECT competency_id, score, assessed_at 
               FROM competency_scores 
               ORDER BY assessed_at DESC"""
        ).fetchall()
        conn.close()

        # Group by competency and check trend
        competency_trends = {}
        for comp_id, score, assessed_at in rows:
            if comp_id not in competency_trends:
                competency_trends[comp_id] = []
            competency_trends[comp_id].append((score, assessed_at))

        emerging_gaps = []
        for comp_id, scores in competency_trends.items():
            if len(scores) >= 2:
                first_score = scores[0][0]
                last_score = scores[-1][0]
                if last_score < first_score * 0.9:  # 10% decline
                    emerging_gaps.append({
                        "competency_id": comp_id,
                        "current_avg": round(last_score, 2),
                        "previous_avg": round(first_score, 2),
                        "decline_percent": round(((first_score - last_score) / first_score) * 100, 1),
                        "priority": "high" if (first_score - last_score) > 1.0 else "medium",
                    })

        return {
            "emerging_skill_gaps": sorted(emerging_gaps, key=lambda x: x["decline_percent"], reverse=True),
            "total_emerging": len(emerging_gaps),
        }
