"""Pytest configuration and shared fixtures."""
import os
import sys
import tempfile
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def setup_test_env():
    """Ensure test environment uses a temporary SQLite database."""
    test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    test_db.close()
    os.environ["SQLITE_PATH"] = test_db.name
    yield test_db.name
    try:
        os.unlink(test_db.name)
    except FileNotFoundError:
        pass
