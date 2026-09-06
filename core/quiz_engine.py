"""
Enhanced Quiz Engine — MCQ, subjective, and adaptive quiz generation.
Generates quizzes from learning materials with difficulty calibration
and question categorization.
"""
import json
import os
import sqlite3
import sys
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings
from core.file_processor import FileProcessor
from core.rag import _call_llm  # Reuse LLM caller

settings = get_settings()


class QuizEngine:
    """Generate and manage quizzes from learning materials."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or settings.sqlite_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()
        self.file_processor = FileProcessor()

    def _init_db(self):
        """Create quiz tables in SQLite."""
        conn = sqlite3.connect(self.db_path)
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
        conn.commit()
        conn.close()

    async def generate_mcqs(
        self,
        document_text: str,
        num_questions: int | None = None,
        difficulty: str = "intermediate",
        domain: str | None = None,
    ) -> dict:
        """
        Generate MCQs from learning material text.
        
        Args:
            document_text: Extracted text from uploaded document
            num_questions: Number of questions (default: from settings)
            difficulty: beginner, intermediate, or advanced
            domain: Competency domain for contextual generation
        """
        num_questions = num_questions or settings.default_quiz_questions
        
        # Truncate if needed
        safe_text = document_text[:settings.max_document_chars]

        domain_prompt = ""
        if domain:
            domain_prompt = f"\nFocus on competencies in the '{domain}' domain."

        prompt = f"""You are an AI Assessment Engine for MoSPI (Ministry of Statistics and Programme Implementation), India.{domain_prompt}
Generate {num_questions} Multiple Choice Questions (MCQs) based ONLY on the following learning material.

## Learning Material:
{safe_text}

## Instructions:
1. Generate exactly {num_questions} questions.
2. Each question must have 4 options (A, B, C, D) and 1 correct answer.
3. Vary difficulty: approximately {num_questions // 3} beginner, {num_questions // 3} intermediate, rest advanced.
4. Provide a brief explanation for the correct answer.
5. Classify each question into a competency category (e.g., "survey_design", "sampling").
6. Output MUST be ONLY valid JSON matching this exact structure:
{{
  "quiz_title": "Descriptive quiz title based on the material",
  "difficulty": "{difficulty}",
  "questions": [
    {{
      "question": "The question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "explanation": "Brief explanation.",
      "difficulty": "beginner|intermediate|advanced",
      "category": "competency_id_or_name"
    }}
  ]
}}
DO NOT include markdown formatting. Return ONLY the raw JSON object.
"""

        raw_output = _call_llm(prompt)

        try:
            clean = raw_output.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            parsed = json.loads(clean)

            quiz_id = str(uuid.uuid4())[:8]
            quiz_title = parsed.get("quiz_title", "Quiz on learning material")

            # Save to database
            conn = sqlite3.connect(self.db_path)
            conn.execute(
                "INSERT INTO quizzes (quiz_id, title, source_text, difficulty, domain, num_questions) VALUES (?, ?, ?, ?, ?, ?)",
                (quiz_id, quiz_title, safe_text[:500], difficulty, domain, num_questions),
            )
            for i, q in enumerate(parsed.get("questions", [])):
                conn.execute(
                    "INSERT INTO quiz_questions (quiz_id, question, options, correct_answer, explanation, difficulty, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (quiz_id, q["question"], json.dumps(q["options"]),
                     str(q["correct_answer"]), q.get("explanation", ""),
                     q.get("difficulty", difficulty), q.get("category", "")),
                )
            conn.commit()
            conn.close()

            return {
                "status": "success",
                "quiz_id": quiz_id,
                "quiz_title": quiz_title,
                "questions": parsed.get("questions", []),
            }

        except Exception as e:  # noqa: BLE001
            return {
                "status": "error",
                "message": f"Failed to generate quiz: {e!s}",
                "raw_output": raw_output[:500],
            }

    async def generate_from_file(
        self,
        file_path: str,
        file_type: str,
        num_questions: int | None = None,
        difficulty: str = "intermediate",
        domain: str | None = None,
    ) -> dict:
        """Generate quiz from an uploaded file (PDF, DOCX, PPTX, etc.)."""
        text = await self.file_processor.process_file(file_path, file_type)
        if not text.strip():
            return {"status": "error", "message": "No text extracted from file"}
        return await self.generate_mcqs(text, num_questions, difficulty, domain)

    async def get_quiz(self, quiz_id: str) -> dict:
        """Retrieve a quiz by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        quiz = conn.execute(
            "SELECT * FROM quizzes WHERE quiz_id = ?", (quiz_id,)
        ).fetchone()
        if not quiz:
            conn.close()
            return None

        questions = conn.execute(
            "SELECT * FROM quiz_questions WHERE quiz_id = ?", (quiz_id,)
        ).fetchall()
        conn.close()

        return {
            "quiz": dict(quiz),
            "questions": [dict(q) for q in questions],
        }

    def calculate_score(self, answers: dict, quiz_questions: list[dict]) -> dict:
        """
        Calculate quiz score from submitted answers.
        
        Args:
            answers: {question_id: selected_option_index}
            quiz_questions: List of quiz question dicts with correct_answer
        
        Returns:
            {score, total, percentage, results: [{question, correct, selected, correct}]}
        """
        total = len(quiz_questions)
        correct = 0
        results = []

        for q in quiz_questions:
            selected = answers.get(str(q["id"]), -1)
            is_correct = int(selected) == int(q["correct_answer"])
            if is_correct:
                correct += 1
            results.append({
                "question": q.get("question", ""),
                "correct": is_correct,
                "selected_option": selected,
                "correct_option": int(q["correct_answer"]),
                "explanation": q.get("explanation", ""),
            })

        return {
            "score": correct,
            "total": total,
            "percentage": round((correct / total * 100) if total > 0 else 0, 1),
            "passed": (correct / total >= 0.6) if total > 0 else False,
            "results": results,
        }
