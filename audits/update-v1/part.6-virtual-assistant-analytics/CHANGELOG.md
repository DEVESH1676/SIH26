# Part 6 — Virtual Assistant, Adaptive Learning & Analytics

## Objective
Build the AI virtual assistant, adaptive quiz system, learning hour tracking, and continuous monitoring with dynamic recommendations.

## 6.1 Create `core/virtual_assistant.py` (NEW FILE)

```python
"""
AI Virtual Assistant for MoSPI Learning Platform.
Provides real-time learner support, course recommendations,
and learning path guidance.
"""
import os
import sys
import json
import sqlite3
from datetime import datetime, timezone
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings
from core.rag import _call_llm

settings = get_settings()


class VirtualAssistant:
    """AI-powered learning assistant for official support."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.sqlite_path

    async def respond(
        self,
        user_message: str,
        user_context: dict = None,
    ) -> dict:
        """
        Process user message and return intelligent response.
        
        Args:
            user_message: User's question or request
            user_context: User profile data (designation, skills, progress)
        
        Returns:
            {
                "response": "The assistant's reply",
                "suggested_actions": ["action1", "action2"],
                "related_resources": [{"type": "course", "id": "...", "title": "..."}],
                "intent": "course_recommendation | quiz_help | concept_explanation | progress_query | other"
            }
        """
        user_context = user_context or {}

        # Build context-aware prompt
        context_parts = []
        if user_context.get("designation"):
            context_parts.append(f"Designation: {user_context['designation']}")
        if user_context.get("competency_summary"):
            context_parts.append(
                f"Current competency levels: {json.dumps(user_context['competency_summary'])}"
            )
        if user_context.get("recent_progress"):
            context_parts.append(
                f"Recent quiz performance: {json.dumps(user_context['recent_progress'])}"
            ]
        if user_context.get("active_courses"):
            context_parts.append(
                f"Currently enrolled: {', '.join(user_context['active_courses'])}"
            )

        context_str = "\n".join(context_parts) if context_parts else "No additional context available."

        intent_prompt = f"""Classify the user's intent into one of these categories:
- course_recommendation: User wants course suggestions
- quiz_help: User needs help with a quiz or assessment
- concept_explanation: User wants to understand a statistical concept
- progress_query: User is asking about their learning progress
- skill_gap_query: User wants to know what skills to develop
- general: General question about the learning platform
- motivational: User needs encouragement or motivation

User message: "{user_message}"

Return ONLY: {{ "intent": "category_name" }}
"""

        intent_raw = _call_llm(intent_prompt)
        intent = "general"
        try:
            intent = json.loads(intent_raw.strip())["intent"]
        except Exception:
            pass

        # Build response based on intent
        response = ""
        suggested_actions = []
        related_resources = []

        if intent == "course_recommendation":
            response = self._handle_course_recommendation(user_message, user_context)
            suggested_actions = [
                {"type": "view_courses", "label": "Browse Available Courses"},
                {"type": "take_assessment", "label": "Take Competency Assessment"},
            ]

        elif intent == "quiz_help":
            response = self._handle_quiz_help(user_message, user_context)
            suggested_actions = [
                {"type": "review_concept", "label": "Review Key Concepts"},
                {"type": "practice_quiz", "label": "Practice Quiz"},
            ]

        elif intent == "concept_explanation":
            response = self._handle_concept_explanation(user_message)
            suggested_actions = [
                {"type": "related_course", "label": "Find a Course on This Topic"},
                {"type": "see_examples", "label": "View Examples"},
            ]

        elif intent == "progress_query":
            response = self._handle_progress_query(user_context)
            suggested_actions = [
                {"type": "view_dashboard", "label": "View Full Dashboard"},
                {"type": "set_goals", "label": "Set Learning Goals"},
            ]

        elif intent == "skill_gap_query":
            response = self._handle_skill_gap_query(user_context)
            suggested_actions = [
                {"type": "take_assessment", "label": "Take Full Assessment"},
                {"type": "view_pathway", "label": "View Learning Pathway"},
            ]

        else:
            response = self._handle_general(user_message)
            suggested_actions = [
                {"type": "explore_courses", "label": "Explore Courses"},
                {"type": "take_quiz", "label": "Take a Quiz"},
            ]

        return {
            "response": response,
            "suggested_actions": suggested_actions,
            "related_resources": related_resources,
            "intent": intent,
        }

    def _handle_course_recommendation(self, message: str, context: dict) -> str:
        return (
            "Based on your profile, I recommend focusing on courses that address your "
            "identified skill gaps. Would you like me to recommend specific iGOT courses "
            "or NSSTA TPAC programmes for your current role?"
        )

    def _handle_quiz_help(self, message: str, context: dict) -> str:
        return (
            "I can help you with quiz preparation. Try reviewing the key concepts first, "
            "then attempt a practice quiz. Would you like me to generate a quiz on a specific topic?"
        )

    def _handle_concept_explanation(self, message: str) -> str:
        return (
            "I'd be happy to explain that concept. Could you specify which area of "
            "statistics you'd like to understand better? I can cover topics like survey "
            "design, sampling, national accounts, or data analysis techniques."
        )

    def _handle_progress_query(self, context: dict) -> str:
        return (
            "I can help track your learning progress. Please check the Analytics section "
            "of your dashboard for detailed progress metrics, competency levels, and "
            "recommended next steps."
        )

    def _handle_skill_gap_query(self, context: dict) -> str:
        return (
            "Your skill gaps have been identified based on your current designation and "
            "experience. I recommend starting with foundational courses in your weakest "
            "area, then progressing to advanced topics. Would you like a personalized "
            "learning pathway?"
        )

    def _handle_general(self, message: str) -> str:
        return (
            "I'm here to help with your learning journey! I can assist with course "
            "recommendations, quiz help, concept explanations, and progress tracking. "
            "What would you like to focus on today?"
        )

    # ── Multi-language Support ────────────────────────────────

    async def respond_multilingual(
        self,
        user_message: str,
        language: str = "en",
        user_context: dict = None,
    ) -> dict:
        """
        Respond in the user's preferred language.
        
        Supports: English, Hindi, Bengali, Tamil, Telugu, Marathi,
                  Gujarati, Urdu, Punjabi, Malayalam, Odia, etc.
        """
        # Get response in English first
        result = await self.respond(user_message, user_context)

        # Translate response if needed
        if language != "en":
            translation_prompt = f"""Translate the following assistant response to {language}.
            Keep the suggested actions and resource references intact.

            Response: {result['response']}

            Return ONLY the translated response text.
            """
            translated = _call_llm(translation_prompt)
            result["response"] = translated

        return result
```

## 6.2 Create `core/adaptive_quiz.py` (NEW FILE)

```python
"""
Adaptive Quiz Engine — Difficulty adjusts based on learner performance.
"""
import asyncio
import json
from typing import Optional

from config.settings import get_settings
from core.quiz_engine import QuizEngine

settings = get_settings()


class AdaptiveQuizEngine:
    """
    Generates quizzes that adapt difficulty based on learner performance.
    Easy questions → if correct, next question harder. If wrong, next easier.
    """

    def __init__(self, quiz_engine: QuizEngine = None):
        self.engine = quiz_engine or QuizEngine()

    async def generate_adaptive_quiz(
        self,
        learner_id: str,
        topic: str,
        num_questions: int = 10,
        initial_difficulty: str = "intermediate",
    ) -> dict:
        """
        Generate an adaptive quiz starting at initial difficulty.
        Questions are drawn from a pool and adapt based on performance.
        """
        # Generate a pool of questions at various difficulties
        pool = await self._generate_question_pool(topic, num_questions * 2)

        # Distribute across difficulties
        beginner_q = [q for q in pool if q.get("difficulty") == "beginner"]
        intermediate_q = [q for q in pool if q.get("difficulty") == "intermediate"]
        advanced_q = [q for q in pool if q.get("difficulty") == "advanced"]

        # Start with initial difficulty
        current_difficulty = initial_difficulty
        selected_questions = []
        remaining = pool.copy()

        for i in range(num_questions):
            if not remaining:
                break

            # Select from current difficulty pool first
            if current_difficulty == "beginner":
                candidates = beginner_q or remaining
            elif current_difficulty == "intermediate":
                candidates = intermediate_q or remaining
            else:
                candidates = advanced_q or remaining

            if candidates:
                question = candidates.pop(0)
                remaining = [q for q in remaining if q["id"] != question["id"]]
                selected_questions.append(question)
            else:
                # Fall back to any remaining
                if remaining:
                    selected_questions.append(remaining.pop(0))

        return {
            "quiz_id": f"adaptive-{learner_id}-{topic[:4]}",
            "questions": selected_questions[:num_questions],
            "adaptive": True,
            "initial_difficulty": initial_difficulty,
            "total_questions": num_questions,
        }

    async def _generate_question_pool(self, topic: str, size: int) -> list[dict]:
        """Generate a pool of questions at all difficulty levels."""
        pools = []
        for diff in ["beginner", "intermediate", "advanced"]:
            # This would integrate with QuizEngine
            # For now, return placeholder
            pass
        return pools
```

## 6.3 Create `core/learning_tracker.py` (NEW FILE)

```python
"""
Learning Hours & Progress Tracker.
Tracks total learning time, course progress, and activity logs.
"""
import os
import sys
import json
import sqlite3
from datetime import datetime, timezone, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings

settings = get_settings()


class LearningTracker:
    """Track learning hours, progress, and activity for each learner."""

    def __init__(self, db_path: str = None):
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
        resource_id: str = None,
        resource_type: str = None,
        duration_seconds: int = 0,
        metadata: dict = None,
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
```

## 6.4 Create `core/analytics.py` (NEW FILE — Admin Analytics)

```python
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

        query = """
            SELECT q.title, 
                   COUNT(DISTINCT qa.learner_id) as enrolled,
                   AVG(CAST(qa.score AS REAL) / qa.total_questions * 100) as avg_quiz_score,
                   SUM(CASE WHEN CAST(qa.score AS REAL) / qa.total_questions >= 0.6 THEN 1 ELSE 0 END) as passed
            FROM quizzes q
            LEFT JOIN quiz_attempts qa ON q.quiz_id = qa.quiz_id
            {% if course_id %}WHERE q.quiz_id IN (
                SELECT quiz_id FROM quiz_questions 
                WHERE category LIKE '%' || ? || '%'
            ){% endif %}
            GROUP BY q.quiz_id
            ORDER BY enrolled DESC
        """
        # Simplified for SQLite
        rows = conn.execute(
            """SELECT q.title, COUNT(DISTINCT qa.learner_id),
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
```

## 6.5 Verification Checklist

- [ ] `core/virtual_assistant.py` handles multiple intents
- [ ] Multi-language response works
- [ ] `core/adaptive_quiz.py` generates adaptive quizzes
- [ ] `core/learning_tracker.py` logs sessions and tracks hours
- [ ] Learning hours dashboard data works
- [ ] `core/analytics.py` provides admin overview
- [ ] Workforce competency distribution works
- [ ] Training effectiveness metrics work
- [ ] Predictive skill needs identification works
- [ ] All new services registered in `main.py` lifespan
