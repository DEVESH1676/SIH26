"""
Comprehensive tests for LearningTracker (core/learning_tracker.py).
Tests activity logging, learning hours calculation, course progress tracking.
"""
import os
import sys
import tempfile
import sqlite3
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def learning_tracker_fixture():
    """Create a fresh temp DB for each test and return a LearningTracker instance."""
    import tempfile
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    
    from config.settings import get_settings
    original_path = get_settings().sqlite_path
    get_settings().sqlite_path = db_path
    
    from core.database import init_db
    init_db()
    
    from core.learning_tracker import LearningTracker
    tracker = LearningTracker(db_path=db_path)
    
    yield tracker
    
    # Cleanup
    try:
        os.unlink(db_path)
    except FileNotFoundError:
        pass
    get_settings().sqlite_path = original_path


class TestLogActivity:
    """Test logging learning activities."""

    def test_log_basic_activity(self, learning_tracker_fixture):
        session_id = learning_tracker_fixture.log_activity(
            learner_id="l1", activity_type="quiz",
            resource_id="q1", resource_type="quiz",
            duration_seconds=120
        )
        assert session_id is not None
        assert isinstance(session_id, str)

    def test_log_activity_without_metadata(self, learning_tracker_fixture):
        session_id = learning_tracker_fixture.log_activity(
            learner_id="l1", activity_type="reading"
        )
        assert session_id is not None

    def test_log_activity_with_metadata(self, learning_tracker_fixture):
        session_id = learning_tracker_fixture.log_activity(
            learner_id="l1", activity_type="reading",
            metadata={"page": 5, "chapter": "Introduction"}
        )
        assert session_id is not None

    def test_log_activity_creates_records(self, learning_tracker_fixture):
        learning_tracker_fixture.log_activity("l1", "quiz", "q1", "quiz", 120)
        learning_tracker_fixture.log_activity("l1", "reading", "doc1", "document", 300)
        hours = learning_tracker_fixture.get_learning_hours("l1")
        assert hours["total_sessions"] == 2


class TestGetLearningHours:
    """Test learning hours calculation."""

    def test_empty_learning_hours(self, learning_tracker_fixture):
        hours = learning_tracker_fixture.get_learning_hours("nonexistent")
        assert hours["total_sessions"] == 0
        assert hours["total_hours"] == 0
        assert hours["average_session_minutes"] == 0

    def test_total_hours_calculation(self, learning_tracker_fixture):
        learning_tracker_fixture.log_activity("l1", "quiz", "q1", "quiz", 3600)  # 1 hour
        hours = learning_tracker_fixture.get_learning_hours("l1")
        assert hours["total_hours"] == 1.0
        assert hours["total_sessions"] == 1

    def test_multiple_sessions_hours(self, learning_tracker_fixture):
        learning_tracker_fixture.log_activity("l1", "quiz", "q1", "quiz", 1800)  # 30 min
        learning_tracker_fixture.log_activity("l1", "reading", "d1", "doc", 3600)  # 1 hour
        hours = learning_tracker_fixture.get_learning_hours("l1")
        assert hours["total_hours"] == 1.5
        assert hours["total_sessions"] == 2

    def test_average_session_duration(self, learning_tracker_fixture):
        learning_tracker_fixture.log_activity("l1", "quiz", "q1", "quiz", 120)   # 2 min
        learning_tracker_fixture.log_activity("l1", "quiz", "q2", "quiz", 180)   # 3 min
        hours = learning_tracker_fixture.get_learning_hours("l1")
        assert hours["average_session_minutes"] == 2.5

    def test_period_filtering(self, learning_tracker_fixture):
        conn = sqlite3.connect(learning_tracker_fixture.db_path)
        import uuid
        from datetime import datetime, timezone, timedelta
        past_date = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        conn.execute("INSERT INTO learning_sessions (session_id, learner_id, activity_type, duration_seconds, started_at) VALUES (?, ?, ?, ?, ?)",
                     (str(uuid.uuid4())[:8], "l1", "quiz", 3600, past_date))
        conn.commit()
        conn.close()
        
        # Get hours for 1 day - should return 0 since the session was 2 days ago
        hours = learning_tracker_fixture.get_learning_hours("l1", period_days=1)
        assert hours["total_hours"] == 0.0

    def test_learning_hours_returns_expected_keys(self, learning_tracker_fixture):
        learning_tracker_fixture.log_activity("l1", "quiz", "q1", "quiz", 60)
        hours = learning_tracker_fixture.get_learning_hours("l1")
        for key in ["total_sessions", "total_hours", "average_session_minutes"]:
            assert key in hours


class TestUpdateCourseProgress:
    """Test course progress tracking."""

    def test_update_progress(self, learning_tracker_fixture):
        learning_tracker_fixture.update_course_progress("l1", "course1", 50.0)
        dashboard = learning_tracker_fixture.get_learner_dashboard_data("l1")
        assert len(dashboard["course_progress"]) == 1
        assert dashboard["course_progress"][0]["progress"] == 50.0

    def test_update_progress_replaces(self, learning_tracker_fixture):
        learning_tracker_fixture.update_course_progress("l1", "course1", 50.0)
        learning_tracker_fixture.update_course_progress("l1", "course1", 80.0)
        dashboard = learning_tracker_fixture.get_learner_dashboard_data("l1")
        assert len(dashboard["course_progress"]) == 1
        assert dashboard["course_progress"][0]["progress"] == 80.0

    def test_progress_complete(self, learning_tracker_fixture):
        learning_tracker_fixture.update_course_progress("l1", "course1", 100.0)
        dashboard = learning_tracker_fixture.get_learner_dashboard_data("l1")
        assert dashboard["course_progress"][0]["completed_at"] is not None

    def test_progress_not_complete(self, learning_tracker_fixture):
        learning_tracker_fixture.update_course_progress("l1", "course1", 75.0)
        dashboard = learning_tracker_fixture.get_learner_dashboard_data("l1")
        assert dashboard["course_progress"][0]["completed_at"] is None

    def test_multiple_courses_progress(self, learning_tracker_fixture):
        learning_tracker_fixture.update_course_progress("l1", "c1", 50.0)
        learning_tracker_fixture.update_course_progress("l1", "c2", 25.0)
        dashboard = learning_tracker_fixture.get_learner_dashboard_data("l1")
        assert len(dashboard["course_progress"]) == 2


class TestGetLearnerDashboardData:
    """Test dashboard data aggregation."""

    def test_empty_dashboard(self, learning_tracker_fixture):
        data = learning_tracker_fixture.get_learner_dashboard_data("nonexistent")
        assert data["learning_hours"]["total_sessions"] == 0
        assert data["course_progress"] == []
        assert data["competency_scores"] == []

    def test_dashboard_with_data(self, learning_tracker_fixture):
        learning_tracker_fixture.log_activity("l1", "quiz", "q1", "quiz", 300)
        learning_tracker_fixture.update_course_progress("l1", "c1", 50.0)
        conn = sqlite3.connect(learning_tracker_fixture.db_path)
        conn.execute(
            "INSERT INTO competency_scores (learner_id, competency_id, score) VALUES (?, ?, ?)",
            ("l1", "STAT-001", 4.0)
        )
        conn.commit()
        conn.close()

        data = learning_tracker_fixture.get_learner_dashboard_data("l1")
        assert data["learning_hours"]["total_sessions"] == 1
        assert len(data["course_progress"]) == 1
        assert len(data["competency_scores"]) == 1

    def test_dashboard_keys(self, learning_tracker_fixture):
        data = learning_tracker_fixture.get_learner_dashboard_data("l1")
        for key in ["learning_hours", "course_progress", "competency_scores"]:
            assert key in data
