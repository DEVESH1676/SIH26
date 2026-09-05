"""Security utilities — sanitization, rate limiting, audit logging."""
import re, time, logging
from collections import defaultdict
from config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)
_audit_db_initialized = False

def init_audit_db():
    """Initialize audit_log table (idempotent, runs only once)."""
    global _audit_db_initialized
    if _audit_db_initialized:
        return
    import sqlite3
    conn = sqlite3.connect(settings.sqlite_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            user_id TEXT NOT NULL,
            resource TEXT,
            details TEXT,
            logged_at TIMESTAMP NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    _audit_db_initialized = True

class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)
        
    def is_allowed(self, key: str) -> bool:
        now = time.time()
        self.requests[key] = [t for t in self.requests[key] if now - t < self.window]
        if len(self.requests[key]) >= self.max_requests:
            return False
        self.requests[key].append(now)
        return True

def sanitize_llm_input(text: str, max_length: int = 50000) -> str:
    if not text:
        return ""
    text = text[:max_length]
    # Remove system prompt injections that start at the beginning of text.
    # Match the injection block (marker + content) and strip it, preserving
    # normal text that follows (identified by a capitalized word after . ).
    text = re.sub(
        r'(system|prompt)[^:]*:\s*(.+?)(?=\.\s+[A-Z]|\.\s+[A-Z][a-z]+|$)',
        '', text,
        flags=re.IGNORECASE | re.DOTALL
    )
    # Also handle "ignore previous" type injections
    text = re.sub(
        r'ignore previous\s*.*?(?=\.\s+[A-Z]|\.\s+[A-Z][a-z]+|$)',
        '', text,
        flags=re.IGNORECASE | re.DOTALL
    )
    text = text.replace('```', '')
    return text.strip()

def audit_log(action: str, user_id: str, resource: str = None, details: dict = None):
    import sqlite3, json
    from datetime import datetime, timezone
    init_audit_db()
    conn = sqlite3.connect(settings.sqlite_path)
    conn.execute(
        "INSERT INTO audit_log (action, user_id, resource, details, logged_at) VALUES (?, ?, ?, ?, ?)",
        (action, user_id, resource, json.dumps(details or {}), datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()
    logger.info(f"AUDIT: {action} by {user_id} on {resource}")
