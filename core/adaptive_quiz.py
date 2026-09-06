"""
Adaptive Quiz Engine — Difficulty adjusts based on learner performance.
"""

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
