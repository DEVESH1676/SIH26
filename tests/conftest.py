"""Pytest configuration — shared fixtures for backend testing.

Memory-efficient: creates ONE shared temp DB per test module, cleaned up after.
"""
import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Module-level shared DB path (set once per test module)
_db_path = None


def _cleanup(path):
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session")
def _shared_db():
    """Session-scoped temp DB — created ONCE per test module run.
    All tests in that module share it. Cleaned up at session end.
    """
    path = tempfile.mktemp(suffix=".db")
    os.environ["SQLITE_PATH"] = path
    from config.settings import get_settings
    get_settings().sqlite_path = path
    yield path
    _cleanup(path)


@pytest.fixture(autouse=True)
def _reset_settings(_shared_db):
    """Reset settings to use the shared DB for every test."""
    from config.settings import get_settings
    get_settings().sqlite_path = _shared_db
    yield


@pytest.fixture
def shared_db_path(_shared_db):
    """Expose the shared DB path for test code to use."""
    return _shared_db
