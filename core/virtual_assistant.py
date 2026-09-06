"""
AI Virtual Assistant for MoSPI Learning Platform.
Provides real-time learner support, course recommendations,
and learning path guidance.
"""
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings
from core.rag import _call_llm

settings = get_settings()


class VirtualAssistant:
    """AI-powered learning assistant for official support."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or settings.sqlite_path

    async def respond(
        self,
        user_message: str,
        user_context: dict | None = None,
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
            )
        if user_context.get("active_courses"):
            context_parts.append(
                f"Currently enrolled: {', '.join(user_context['active_courses'])}"
            )

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
        except Exception:  # noqa: S110, BLE001
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
        user_context: dict | None = None,
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
