"""
Backend unit tests for core modules.
"""
import pytest
import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.classifier import CompetencyAnalyzer
from core.quiz_engine import QuizEngine
from core.attempt_tracker import AttemptTracker
from core.igot_api import IGOTClient
from core.file_processor import FileProcessor


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class TestCompetencyAnalyzer:
    def test_analyze_competency(self):
        analyzer = CompetencyAnalyzer()
        user_profile = {
            "designation": "Statistical Analyst",
            "experience_years": 3,
            "current_skills": ["data_entry"],
            "domain": "statistical",
        }
        result = analyzer.analyze(user_profile)
        assert result["overall_level"] is not None
        assert "skill_gaps" in result
        assert "recommended_courses" in result


class TestQuizEngine:
    def test_init_db(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".db", delete=True) as f:
            engine = QuizEngine(db_path=f.name)
            assert os.path.exists(f.name)

    def test_calculate_score(self):
        engine = QuizEngine()
        answers = {"1": 0, "2": 1, "3": 2}
        questions = [
            {"id": "1", "correct_answer": "0"},
            {"id": "2", "correct_answer": "1"},
            {"id": "3", "correct_answer": "2"},
        ]
        result = engine.calculate_score(answers, questions)
        assert result["score"] == 3
        assert result["percentage"] == 100.0


class TestFileProcessor:
    def test_txt_processing(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello world. This is a test document.")
        processor = FileProcessor()
        text = asyncio.get_event_loop().run_until_complete(
            processor.process_file(str(test_file), "txt")
        )
        assert "Hello world" in text

    def test_unsupported_type(self, tmp_path):
        test_file = tmp_path / "test.xyz"
        test_file.write_text("content")
        processor = FileProcessor()
        with pytest.raises(ValueError):
            asyncio.get_event_loop().run_until_complete(
                processor.process_file(str(test_file), "xyz")
            )


class TestIGOTClient:
    def test_init(self):
        client = IGOTClient()
        assert client.base_url is not None
        assert client._headers is not None


class TestAttemptTracker:
    def test_record_and_retrieve(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".db", delete=True) as f:
            tracker = AttemptTracker(db_path=f.name)
            attempt_id = tracker.record_attempt(
                quiz_id="test-quiz", learner_id="learner-1",
                answers={"1": 0}, score=1, total=1,
                time_taken_seconds=30,
            )
            history = tracker.get_learner_history("learner-1")
            assert len(history) == 1
            assert history[0]["score"] == 1

    def test_performance_aggregation(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".db", delete=True) as f:
            tracker = AttemptTracker(db_path=f.name)
            tracker.record_attempt("q1", "l1", {"1": 0}, 1, 1, 30)
            tracker.record_attempt("q2", "l1", {"1": 0}, 2, 2, 60)
            perf = tracker.get_learner_performance("l1")
            assert perf["total_attempts"] == 2
            assert perf["average_score"] == 85.0  # (100 + 75) / 2
