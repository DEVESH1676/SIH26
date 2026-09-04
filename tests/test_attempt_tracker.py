"""Tests for AttemptTracker (core/attempt_tracker.py)."""
import sys, os, pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def shared_db_path(_shared_db):
    """Expose shared DB path and init the database."""
    from core.database import init_db
    init_db()
    return _shared_db


class TestRecordAttempt:
    def test_record_basic(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        aid = t.record_attempt("q1", "l1", {"1": 0}, 1, 1, 30)
        assert aid is not None

    def test_ids_unique(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        t.record_attempt("q1", "l1", {"1": 0}, 1, 1, 30)
        t.record_attempt("q1", "l1", {"1": 0}, 1, 1, 30)
        h = t.get_learner_history("l1")
        assert len(h) == 2

    def test_different_learners(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        t.record_attempt("q1", "l1", {"1": 0}, 1, 1, 30)
        t.record_attempt("q1", "l2", {"1": 0}, 0, 1, 45)
        assert len(t.get_learner_history("l1")) == 1
        assert len(t.get_learner_history("l2")) == 1

    def test_multiple_answers(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        aid = t.record_attempt("q1", "l1", {"1": 0, "2": 1}, 1, 2, 60)
        assert aid is not None


class TestGetLearnerHistory:
    def test_empty_history(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        assert t.get_learner_history("nope") == []

    def test_history_is_list_of_dicts(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        t.record_attempt("q1", "l1", {"1": 0}, 1, 1, 30)
        h = t.get_learner_history("l1")
        assert isinstance(h, list) and isinstance(h[0], dict)

    def test_history_keys(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        t.record_attempt("test-quiz", "l1", {"1": 0}, 1, 1, 30)
        h = t.get_learner_history("l1")
        keys = set(h[0].keys())
        assert {"attempt_id", "quiz_id", "score", "total", "percentage"}.issubset(keys)

    def test_history_limit(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        for i in range(25):
            t.record_attempt(f"q{i}", "l1", {"1": 0}, 1, 1, 30)
        h = t.get_learner_history("l1", limit=20)
        assert len(h) == 20


class TestPerformance:
    def test_empty_performance(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        p = t.get_learner_performance("nope")
        assert p["total_attempts"] == 0

    def test_single_attempt(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        t.record_attempt("q1", "l1", {"1": 0}, 1, 1, 30)
        p = t.get_learner_performance("l1")
        assert p["total_attempts"] == 1
        assert p["average_score"] == 100.0
        assert p["pass_rate"] == 100.0

    def test_multiple_attempts(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        t.record_attempt("q1", "l1", {"1": 0}, 1, 1, 30)   # 100%
        t.record_attempt("q2", "l1", {"1": 0}, 0, 1, 60)    # 0%
        p = t.get_learner_performance("l1")
        assert p["total_attempts"] == 2
        assert p["best_score"] == 100.0
        assert p["worst_score"] == 0.0
        assert p["pass_rate"] == 50.0

    def test_pass_threshold(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        t.record_attempt("q1", "l1", {"1": 0}, 6, 10, 60)  # 60% pass
        p = t.get_learner_performance("l1")
        assert p["passed_count"] == 1

    def test_keys(self, shared_db_path):
        from core.attempt_tracker import AttemptTracker
        t = AttemptTracker(db_path=shared_db_path)
        t.record_attempt("q1", "l1", {"1": 0}, 1, 1, 30)
        p = t.get_learner_performance("l1")
        assert "average_time_seconds" in p
