"""
Comprehensive tests for Analytics (core/analytics.py).
Tests admin overview, workforce competency, training effectiveness, predictive skill needs.
"""
import os
import sys
import tempfile
import sqlite3
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def analytics_db():
    """Create a fresh temp DB with analytics test data for each test."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    from config.settings import get_settings
    original_path = get_settings().sqlite_path
    get_settings().sqlite_path = db_path
    # Also set on core.database module-level settings (init_db reads from there)
    from core.database import settings as db_settings
    original_db_path = db_settings.sqlite_path
    db_settings.sqlite_path = db_path

    from core.database import init_db
    init_db()

    conn = sqlite3.connect(db_path)

    # Insert test data for analytics
    # Create a quiz and questions (required for training_effectiveness)
    conn.execute(
        "INSERT INTO quizzes (quiz_id, title, source_text, difficulty, domain, num_questions) VALUES (?, ?, ?, ?, ?, ?)",
        ("quiz-1", "Statistical Basics", "Test material", "beginner", "statistical", 5),
    )
    for i in range(5):
        conn.execute(
            "INSERT INTO quiz_questions (quiz_id, question, options, correct_answer, explanation, difficulty, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("quiz-1", f"Question {i+1}", '["A","B","C","D"]', "0", "Explanation", "beginner", "stats"),
        )
    conn.commit()

    # Create learning sessions for 2 learners
    import uuid
    for learner_id, num_sessions in [("learner-1", 1), ("learner-2", 1)]:
        for _ in range(num_sessions):
            conn.execute(
                "INSERT INTO learning_sessions (session_id, learner_id, activity_type, duration_seconds, started_at, completed_at) VALUES (?, ?, ?, ?, ?, ?)",
                (str(uuid.uuid4())[:8], learner_id, "quiz", 300, "2025-01-01T00:00:00", "2025-01-01T00:05:00"),
            )
    conn.commit()

    # Create quiz attempts for 3 learners (for training_effectiveness: 3 enrolled, 1 pass, avg ~46.67)
    # Score 3/5 = 60% (pass), 2/5 = 40% (fail), 2/5 = 40% (fail)
    for attempt_num, (learner_id, score, total) in enumerate([
        ("learner-1", 3, 5),  # 60% - pass
        ("learner-2", 2, 5),  # 40% - fail
        ("learner-3", 2, 5),  # 40% - fail
    ], 1):
        conn.execute(
            "INSERT INTO quiz_attempts (attempt_id, quiz_id, learner_id, answers, score, total_questions, time_taken_seconds, started_at, completed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (f"attempt-{attempt_num}", "quiz-1", learner_id, '{"1":"0","2":"0","3":"0","4":"1","5":"1"}',
             score, total, 300, "2025-01-01T01:00:00", "2025-01-01T01:05:00"),
        )
    conn.commit()

    # Create enrolled course progress
    conn.execute(
        "INSERT INTO learner_progress (learner_id, course_id, progress_percent, last_accessed) VALUES (?, ?, ?, ?)",
        ("learner-1", "course-1", 50.0, "2025-01-01T00:00:00"),
    )
    conn.commit()

    # Create competency scores (at least 2 for workforce_competency)
    for comp_id, score in [("STAT-001", 4.0), ("TECH-001", 3.5)]:
        conn.execute(
            "INSERT INTO competency_scores (learner_id, competency_id, score, assessed_at) VALUES (?, ?, ?, ?)",
            ("learner-1", comp_id, score, "2025-01-01T00:00:00"),
        )
    conn.commit()

    conn.close()

    from core.analytics import LearningAnalytics
    analytics = LearningAnalytics(db_path=db_path)

    try:
        yield analytics
    finally:
        try:
            os.unlink(db_path)
        except FileNotFoundError:
            pass
        get_settings().sqlite_path = original_path
        db_settings.sqlite_path = original_db_path


class TestAdminOverview:
    """Test admin dashboard overview metrics."""

    def test_total_learners(self, analytics_db):
        overview = analytics_db.get_admin_overview()
        assert overview["total_learners"] == 2  # learner-1, learner-2 have sessions

    def test_total_sessions(self, analytics_db):
        overview = analytics_db.get_admin_overview()
        assert overview["total_learning_sessions"] == 2

    def test_total_quiz_attempts(self, analytics_db):
        overview = analytics_db.get_admin_overview()
        assert overview["total_quiz_attempts"] == 3

    def test_total_courses(self, analytics_db):
        overview = analytics_db.get_admin_overview()
        assert overview["total_enrolled_courses"] == 1

    def test_overview_has_period(self, analytics_db):
        overview = analytics_db.get_admin_overview()
        assert "period" in overview
        assert overview["period"] == "all_time"

    def test_overview_all_numeric(self, analytics_db):
        overview = analytics_db.get_admin_overview()
        for key in ["total_learners", "total_learning_sessions", "total_quiz_attempts", "total_enrolled_courses"]:
            assert isinstance(overview[key], int), f"{key} should be int, got {type(overview[key])}"


class TestWorkforceCompetency:
    """Test workforce competency distribution analysis."""

    def test_returns_competencies_list(self, analytics_db):
        result = analytics_db.get_workforce_competency_distribution()
        assert "competencies" in result
        assert isinstance(result["competencies"], list)
        assert len(result["competencies"]) >= 2

    def test_competency_has_expected_keys(self, analytics_db):
        result = analytics_db.get_workforce_competency_distribution()
        comp = result["competencies"][0]
        for key in ["competency_id", "avg_score", "assessed_count", "mastery_rate"]:
            assert key in comp

    def test_mastery_rate_calculation(self, analytics_db):
        result = analytics_db.get_workforce_competency_distribution()
        for comp in result["competencies"]:
            assert 0 <= comp["mastery_rate"] <= 100

    def test_competencies_sorted_by_avg_score(self, analytics_db):
        result = analytics_db.get_workforce_competency_distribution()
        scores = [c["avg_score"] for c in result["competencies"]]
        # Should be sorted descending
        assert scores == sorted(scores, reverse=True)


class TestTrainingEffectiveness:
    """Test training effectiveness metrics."""

    def test_returns_courses_list(self, analytics_db):
        result = analytics_db.get_training_effectiveness()
        assert "courses" in result
        assert isinstance(result["courses"], list)
        assert len(result["courses"]) >= 1

    def test_course_has_expected_keys(self, analytics_db):
        result = analytics_db.get_training_effectiveness()
        course = result["courses"][0]
        for key in ["title", "enrolled", "avg_score", "pass_rate"]:
            assert key in course

    def test_enrolled_count(self, analytics_db):
        result = analytics_db.get_training_effectiveness()
        for course in result["courses"]:
            assert course["enrolled"] == 3  # 3 learners attempted

    def test_pass_rate_calculation(self, analytics_db):
        result = analytics_db.get_training_effectiveness()
        for course in result["courses"]:
            # 1 of 3 learners passed (score >= 60%)
            assert course["pass_rate"] == 33.3

    def test_avg_score_calculation(self, analytics_db):
        result = analytics_db.get_training_effectiveness()
        # Scores: 3/5=60%, 2/5=40%, 2/5=40% -> avg = 46.67%
        for course in result["courses"]:
            assert 45 <= course["avg_score"] <= 50


class TestPredictiveSkillNeeds:
    """Test predictive skill gap analysis."""

    def test_returns_expected_keys(self, analytics_db):
        result = analytics_db.get_predictive_skill_needs()
        assert "emerging_skill_gaps" in result
        assert "total_emerging" in result

    def test_total_emerging_matches_list(self, analytics_db):
        result = analytics_db.get_predictive_skill_needs()
        assert result["total_emerging"] == len(result["emerging_skill_gaps"])

    def test_gap_has_expected_keys(self, analytics_db):
        result = analytics_db.get_predictive_skill_needs()
        if result["emerging_skill_gaps"]:
            gap = result["emerging_skill_gaps"][0]
            for key in ["competency_id", "current_avg", "previous_avg", "decline_percent", "priority"]:
                assert key in gap

    def test_priority_is_valid(self, analytics_db):
        result = analytics_db.get_predictive_skill_needs()
        for gap in result["emerging_skill_gaps"]:
            assert gap["priority"] in ["high", "medium"]

    def test_decline_percent_positive(self, analytics_db):
        result = analytics_db.get_predictive_skill_needs()
        for gap in result["emerging_skill_gaps"]:
            assert gap["decline_percent"] > 0

    def test_empty_db_returns_empty_list(self):
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        from config.settings import get_settings
        get_settings().sqlite_path = db_path
        from core.learning_tracker import LearningTracker
        LearningTracker(db_path=db_path)
        from core.analytics import LearningAnalytics
        analytics = LearningAnalytics(db_path=db_path)
        result = analytics.get_predictive_skill_needs()
        assert result["emerging_skill_gaps"] == []
        assert result["total_emerging"] == 0

        os.unlink(db_path)
