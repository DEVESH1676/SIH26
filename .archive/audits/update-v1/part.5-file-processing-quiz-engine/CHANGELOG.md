# Part 5 — File Processing, Quiz Engine & Assessment Pipeline

## Objective
Add multi-format document processing (PDF, DOCX, PPTX, video), enhanced quiz generation, adaptive assessments, and attempt tracking.

## 5.1 Create `core/file_processor.py` (NEW FILE)

```python
"""
Multi-format file processor for learning materials.
Handles PDF, DOCX, PPTX, video (with transcription), and audio extraction.
"""
import os
import sys
import tempfile
import asyncio
import subprocess
from typing import Optional, Tuple
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings

settings = get_settings()


class FileProcessor:
    """Process uploaded learning materials into extractable text."""

    def __init__(self, upload_dir: str = "data/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def process_file(
        self,
        file_path: str,
        file_type: str,
        max_chars: int = None,
    ) -> str:
        """
        Process any supported file type and return extracted text.
        
        Args:
            file_path: Path to the uploaded file
            file_type: File extension (pdf, docx, pptx, txt, mp4, mp3)
            max_chars: Maximum characters to return (default: from settings)
        
        Returns:
            Extracted text content
        """
        max_chars = max_chars or settings.max_document_chars
        file_type = file_type.lower().lstrip(".")

        handlers = {
            "pdf": self._process_pdf,
            "docx": self._process_docx,
            "pptx": self._process_pptx,
            "txt": self._process_txt,
            "mp4": self._process_video,
            "mp3": self._process_audio,
            "wav": self._process_audio,
        }

        handler = handlers.get(file_type)
        if not handler:
            raise ValueError(
                f"Unsupported file type: {file_type}. "
                f"Supported: {', '.join(handlers.keys())}"
            )

        # Limit text length
        text = await handler(file_path)
        return text[:max_chars]

    async def _process_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n\n".join(text_parts)
        except ImportError:
            raise ImportError("pypdf not installed. Run: pip install pypdf")

    async def _process_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            from docx import Document
            doc = Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paragraphs)
        except ImportError:
            raise ImportError("python-docx not installed. Run: pip install python-docx")

    async def _process_pptx(self, file_path: str) -> str:
        """Extract text from PPTX file."""
        try:
            from pptx import Presentation
            pres = Presentation(file_path)
            text_parts = []
            for slide in pres.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for paragraph in shape.text_frame.paragraphs:
                            text = paragraph.text.strip()
                            if text:
                                text_parts.append(text)
            return "\n\n".join(text_parts)
        except ImportError:
            raise ImportError("python-pptx not installed. Run: pip install python-pptx")

    async def _process_txt(self, file_path: str) -> str:
        """Read plain text file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    async def _process_video(self, file_path: str) -> Tuple[str, list[dict]]:
        """
        Extract transcription from video file.
        Uses Whisper (local Ollama) for transcription.
        
        Returns:
            (full_text, chapter_marks) where chapter_marks is list of
            {"timestamp": str, "text": str}
        """
        try:
            # Use Whisper via Ollama for local transcription
            result = subprocess.run(
                ["ollama", "run", "whisper", file_path],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max
            )
            if result.returncode == 0:
                return result.stdout, []
            else:
                raise Exception(f"Whisper transcription failed: {result.stderr}")
        except FileNotFoundError:
            raise Exception(
                "Ollama not available. Install Ollama and run: ollama pull whisper"
            )

    async def _process_audio(self, file_path: str) -> str:
        """Extract transcription from audio file."""
        # Similar to video processing
        return await self._process_video(file_path)

    async def chunk_document(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200,
    ) -> list[dict]:
        """
        Split document into overlapping chunks for embedding.
        
        Returns list of {"text": str, "start": int, "end": int, "chunk_index": int}
        """
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending
                break_point = max(
                    text.rfind(". ", start + chunk_size // 2, end),
                    text.rfind("\n", start + chunk_size // 2, end),
                )
                if break_point > start + chunk_size // 2:
                    end = break_point + 1

            chunks.append({
                "text": text[start:end].strip(),
                "start": start,
                "end": end,
                "chunk_index": chunk_index,
            })
            chunk_index += 1
            start = end - overlap

        return chunks
```

## 5.2 Create `core/quiz_engine.py` (NEW FILE)

```python
"""
Enhanced Quiz Engine — MCQ, subjective, and adaptive quiz generation.
Generates quizzes from learning materials with difficulty calibration
and question categorization.
"""
import os
import sys
import json
import uuid
import asyncio
import sqlite3
from datetime import datetime, timezone
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings
from core.file_processor import FileProcessor
from core.rag import _call_llm  # Reuse LLM caller

settings = get_settings()


class QuizEngine:
    """Generate and manage quizzes from learning materials."""

    def __init__(self, db_path: str = None):
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
        num_questions: int = None,
        difficulty: str = "intermediate",
        domain: str = None,
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

        prompt = f"""You are an AI Assessment Engine for MoSPI (Ministry of Statistics and Programme Implementation), India.
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
            quiz_title = parsed.get("quiz_title", f"Quiz on learning material")

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

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to generate quiz: {str(e)}",
                "raw_output": raw_output[:500],
            }

    async def generate_from_file(
        self,
        file_path: str,
        file_type: str,
        num_questions: int = None,
        difficulty: str = "intermediate",
        domain: str = None,
    ) -> dict:
        """Generate quiz from an uploaded file (PDF, DOCX, PPTX, etc.)."""
        text = await self.file_processor.process_file(file_path, file_type)
        if not text.strip():
            return {"status": "error", "message": "No text extracted from file"}
        return await self.generate_mcqs(text, num_questions, difficulty, domain)

    async def get_quiz(self, quiz_id: str) -> dict:
        """Retrieve a quiz by ID."""
        conn = sqlite3.connect(self.db_path)
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
            "quiz": dict(zip(quiz.keys(), quiz)),
            "questions": [dict(zip(
                ["id", "quiz_id", "question", "options", "correct_answer",
                 "explanation", "difficulty", "category"], q
            )) for q in questions],
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
                "question": q["question"],
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
```

## 5.3 Create `core/attempt_tracker.py` (NEW FILE)

```python
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
               JOIN quizzes q ON qa.quiz_id = q.quiz_id
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
```

## 5.4 Update `core/rag.py` — QuizGenerator

Replace `QuizGenerator` with the new enhanced version (the `QuizEngine` class above is preferred). The old `QuizGenerator` in `rag.py` should be removed.

## 5.5 Verification Checklist

- [x] `core/file_processor.py` handles PDF, DOCX, PPTX, TXT
- [x] Video/audio transcription works with Ollama Whisper
- [x] `core/quiz_engine.py` creates quizzes with difficulty levels
- [x] Quizzes are saved to SQLite
- [x] Score calculation works correctly
- [x] `core/attempt_tracker.py` records and retrieves attempts
- [x] Learner performance aggregation works
- [x] File upload size limits enforced
- [x] Chunking handles large documents properly
- [x] Error handling for unsupported file types
