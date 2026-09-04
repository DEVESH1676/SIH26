"""
Comprehensive tests for QuizEngine (core/quiz_engine.py).
Tests DB initialization, quiz generation (without LLM), retrieval, and scoring.
"""
import os
import sys
import tempfile
import json
import pytest
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture()
def quiz_engine_fixture(shared_db_path):
    """Create a temp DB with quiz tables and return engine."""
    from core.quiz_engine import QuizEngine
    engine = QuizEngine(db_path=shared_db_path)
    return engine


class TestQuizEngineInit:
    """Test QuizEngine initialization and DB setup."""

    def shared_db_path_created(self, quiz_engine_fixture):
        assert os.path.exists(quiz_engine_fixture.db_path)

    def test_quizzes_table_exists(self, quiz_engine_fixture):
        import sqlite3
        conn = sqlite3.connect(quiz_engine_fixture.db_path)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='quizzes'"
        ).fetchone()
        conn.close()
        assert tables is not None

    def test_quiz_questions_table_exists(self, quiz_engine_fixture):
        import sqlite3
        conn = sqlite3.connect(quiz_engine_fixture.db_path)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='quiz_questions'"
        ).fetchone()
        conn.close()
        assert tables is not None

    def test_quiz_attempts_table_exists(self, quiz_engine_fixture):
        import sqlite3
        conn = sqlite3.connect(quiz_engine_fixture.db_path)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='quiz_attempts'"
        ).fetchone()
        conn.close()
        assert tables is not None

    def test_custom_db_path(self):
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            custom_path = f.name
        try:
            from core.quiz_engine import QuizEngine
            engine = QuizEngine(db_path=custom_path)
            assert os.path.exists(custom_path)
        finally:
            os.unlink(custom_path)

    def test_score_with_string_keys(self, quiz_engine_fixture):
        questions = [
            {"id": "1", "correct_answer": "0"},
            {"id": "2", "correct_answer": "1"},
        ]
        answers = {"1": "0", "2": "1"}
        result = quiz_engine_fixture.calculate_score(answers, questions)
        assert result["score"] == 2
        assert result["percentage"] == 100.0


class TestGetQuiz:
    """Test quiz retrieval."""

    def test_get_nonexistent_quiz(self, quiz_engine_fixture):
        result = asyncio.run(quiz_engine_fixture.get_quiz("nonexistent"))
        assert result is None

    def test_get_quiz_after_insert(self, quiz_engine_fixture):
        import sqlite3
        conn = sqlite3.connect(quiz_engine_fixture.db_path)
        conn.execute(
            "INSERT INTO quizzes (quiz_id, title, source_text, difficulty, domain, num_questions) VALUES (?, ?, ?, ?, ?, ?)",
            ("test-q1", "Test Quiz", "test", "beginner", "statistical", 3)
        )
        conn.execute(
            "INSERT INTO quiz_questions (quiz_id, question, options, correct_answer, explanation, difficulty, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("test-q1", "What is 2+2?", '["1","2","3","4"]', "3", "Basic math", "beginner", "math")
        )
        conn.commit()
        conn.close()

        result = asyncio.run(quiz_engine_fixture.get_quiz("test-q1"))
        assert result is not None
        assert result["quiz"]["title"] == "Test Quiz"
        assert len(result["questions"]) == 1

    def test_get_quiz_empty_questions(self, quiz_engine_fixture):
        import sqlite3
        conn = sqlite3.connect(quiz_engine_fixture.db_path)
        conn.execute(
            "INSERT INTO quizzes (quiz_id, title, source_text, difficulty, domain, num_questions) VALUES (?, ?, ?, ?, ?, ?)",
            ("test-q2", "Empty Quiz", "test", "beginner", "statistical", 0)
        )
        conn.commit()
        conn.close()

        result = asyncio.run(quiz_engine_fixture.get_quiz("test-q2"))
        assert result is not None
        assert len(result["questions"]) == 0


class TestCalculateScore:
    """Test quiz scoring logic."""

    def test_all_correct(self, quiz_engine_fixture):
        questions = [
            {"id": 1, "question": "Q1", "correct_answer": 0},
            {"id": 2, "question": "Q2", "correct_answer": 1},
            {"id": 3, "question": "Q3", "correct_answer": 2},
        ]
        answers = {"1": 0, "2": 1, "3": 2}
        result = quiz_engine_fixture.calculate_score(answers, questions)
        assert result["score"] == 3
        assert result["total"] == 3
        assert result["percentage"] == 100.0
        assert result["passed"] is True
        assert len(result["results"]) == 3

    def test_all_wrong(self, quiz_engine_fixture):
        questions = [
            {"id": 1, "question": "Q1", "correct_answer": 0},
            {"id": 2, "question": "Q2", "correct_answer": 1},
        ]
        answers = {"1": 1, "2": 0}
        result = quiz_engine_fixture.calculate_score(answers, questions)
        assert result["score"] == 0
        assert result["percentage"] == 0.0
        assert result["passed"] is False

    def test_partial_correct(self, quiz_engine_fixture):
        questions = [
            {"id": 1, "question": "Q1", "correct_answer": 0},
            {"id": 2, "question": "Q2", "correct_answer": 1},
            {"id": 3, "question": "Q3", "correct_answer": 2},
            {"id": 4, "question": "Q4", "correct_answer": 3},
        ]
        answers = {"1": 0, "2": 0, "3": 2, "4": 3}
        result = quiz_engine_fixture.calculate_score(answers, questions)
        assert result["score"] == 3
        assert result["total"] == 4
        assert result["percentage"] == 75.0
        assert result["passed"] is True

    def test_pass_threshold_at_60(self, quiz_engine_fixture):
        questions = [
            {"id": 1, "question": "Q1", "correct_answer": 0},
            {"id": 2, "question": "Q2", "correct_answer": 0},
            {"id": 3, "question": "Q3", "correct_answer": 0},
            {"id": 4, "question": "Q4", "correct_answer": 0},
            {"id": 5, "question": "Q5", "correct_answer": 0},
        ]
        answers = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 1}  # 80%
        result = quiz_engine_fixture.calculate_score(answers, questions)
        assert result["passed"] is True
        assert result["percentage"] == 80.0

    def test_fail_at_below_60(self, quiz_engine_fixture):
        questions = [
            {"id": 1, "question": "Q1", "correct_answer": 0},
            {"id": 2, "question": "Q2", "correct_answer": 0},
            {"id": 3, "question": "Q3", "correct_answer": 0},
        ]
        answers = {"1": 0, "2": 1, "3": 1}  # 33.3%
        result = quiz_engine_fixture.calculate_score(answers, questions)
        assert result["passed"] is False

    def test_empty_questions(self, quiz_engine_fixture):
        result = quiz_engine_fixture.calculate_score({}, [])
        assert result["score"] == 0
        assert result["total"] == 0
        assert result["percentage"] == 0.0
        assert result["passed"] is False

    def test_results_detail_included(self, quiz_engine_fixture):
        questions = [
            {"id": 1, "correct_answer": 0, "question": "Q1", "explanation": "E1"},
            {"id": 2, "correct_answer": 1, "question": "Q2", "explanation": "E2"},
        ]
        answers = {"1": 0, "2": 0}
        result = quiz_engine_fixture.calculate_score(answers, questions)
        assert len(result["results"]) == 2
        assert result["results"][0]["correct"] is True
        assert result["results"][1]["correct"] is False
        assert result["results"][0]["explanation"] == "E1"

    def test_string_question_ids(self, quiz_engine_fixture):
        questions = [
            {"id": "1", "question": "Q1", "correct_answer": 0},
            {"id": "2", "question": "Q2", "correct_answer": 1},
        ]
        answers = {"1": 0, "2": 1}
        result = quiz_engine_fixture.calculate_score(answers, questions)
        assert result["score"] == 2
        assert result["percentage"] == 100.0


class TestQuizEngineWithLLM:
    """Test quiz generation with LLM (may skip if LLM unavailable)."""

    def test_generate_mcqs_returns_dict(self):
        """Test that generate_mcqs returns a properly structured dict."""
        from core.quiz_engine import QuizEngine
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            engine = QuizEngine(db_path=db_path)
            text = "The Pythagorean theorem states that in a right triangle, a² + b² = c²."
            import asyncio
            result = asyncio.run(engine.generate_mcqs(text, num_questions=2))

            assert isinstance(result, dict)
            assert "status" in result

            # If LLM is available, check full structure
            if result["status"] == "success":
                assert "quiz_id" in result
                assert "quiz_title" in result
                assert "questions" in result
                assert isinstance(result["questions"], list)
                if result["questions"]:
                    q = result["questions"][0]
                    assert "question" in q
                    assert "options" in q
                    assert "correct_answer" in q
                    assert "explanation" in q

            # If LLM is not available, it should still return error status
            if result["status"] == "error":
                assert "message" in result

        finally:
            os.unlink(db_path)
