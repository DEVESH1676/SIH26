# Part 4: Bug Analysis & Fix Recommendations

## 🔴 Critical Bugs (Fix Immediately)

### BUG-001: Missing `analytics_db` fixture in `test_analytics.py`
- **File:** `tests/test_analytics.py`
- **Lines:** 17, 21, 25, 29, 33, 38, 47, 53, 59, 64, 74, 80, 86, 91, 97, 107, 112, 116, 123, 128
- **Impact:** 20 tests completely non-functional
- **Root Cause:** Tests reference fixture `analytics_db` which is never defined anywhere
- **Fix:** Add fixture to conftest.py or test file:
```python
@pytest.fixture
def analytics_db(shared_db_path):
    from core.database import init_db
    init_db()
    # Insert test data for analytics (quizzes, attempts, sessions, progress)
    from core.learning_tracker import LearningTracker
    from core.analytics import LearningAnalytics
    tracker = LearningTracker(db_path=shared_db_path)
    tracker.log_activity("l1", "quiz", "q1", "quiz", 120)
    tracker.log_activity("l1", "reading", "d1", "doc", 300)
    tracker.update_course_progress("l1", "course1", 50.0)
    analytics = LearningAnalytics(db_path=shared_db_path)
    return analytics
```

### BUG-002: Missing `shared_db_path` fixture in `test_attempt_tracker.py`
- **File:** `tests/test_attempt_tracker.py`
- **Lines:** 15, 21, 29, 37, 45, 50, 57, 65, 75, 81, 90, 101, 108
- **Impact:** 13 tests completely non-functional
- **Root Cause:** Test file defines `_init_db` fixture but methods reference `shared_db_path` which is out of scope. The fixture `_init_db` has no return value to pass to test methods.
- **Fix:** Add explicit fixture:
```python
@pytest.fixture
def shared_db_path(_shared_db):
    from core.database import init_db
    init_db()
    return _shared_db
```

### BUG-003: `require_role()` decorator is a no-op
- **File:** `core/auth.py`
- **Lines:** 109-116
- **Impact:** RBAC enforcement at function level is completely broken
- **Root Cause:** The decorator returns the function unchanged — no role checking logic
```python
def require_role(role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)  # NO CHECK!
        return wrapper
    return decorator
```
- **Fix:** Add actual role permission checking:
```python
def require_role(role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = kwargs.get('request').state.user_id
            roles = get_user_roles(user_id)
            if role not in roles:
                raise HTTPException(status_code=403, detail="Insufficient role")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## 🟠 High Bugs

### BUG-004: `calculate_score()` crashes on missing `question` key
- **File:** `core/quiz_engine.py`
- **Line:** 230
- **Impact:** Quiz scoring crashes if any question lacks `question` field
- **Root Cause:** Direct key access `q["question"]` instead of `.get()`
- **Fix:**
```python
# Change line 230 from:
"question": q["question"],
# To:
"question": q.get("question", ""),
```

### BUG-005: JWT `iat` claim not included in refresh tokens
- **File:** `core/auth.py`
- **Line:** 66-69
- **Impact:** Tests expecting `iat` fail; some JWT libraries require it
- **Root Cause:** `create_refresh_token()` only sets `exp` and `type`, not `iat`
- **Fix:**
```python
def create_refresh_token(data: dict) -> str:
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=settings.jwt_refresh_token_expiry_days
    )
    data["iat"] = datetime.datetime.now(datetime.timezone.utc)
    data["exp"] = expire
    data["type"] = "refresh"
    return jwt.encode(data, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
```

### BUG-006: `get_user_roles()` crashes if `user_roles` table missing
- **File:** `core/auth.py`
- **Line:** 82
- **Impact:** Any code path calling `check_permission()` or `get_user_roles()` crashes if table doesn't exist
- **Root Cause:** No `CREATE TABLE IF NOT EXISTS` before query
- **Fix:** Add table creation or use try/except:
```python
def get_user_roles(user_id: str) -> list[str]:
    import sqlite3
    conn = sqlite3.connect(settings.sqlite_path)
    try:
        rows = conn.execute(
            "SELECT role FROM user_roles WHERE user_id = ?", (user_id,)).fetchall()
        if not rows:
            user_row = conn.execute(
                "SELECT roles FROM users WHERE id = ?", (user_id,)).fetchone()
            if user_row and user_row[0]:
                conn.close()
                return user_row[0].split(",")
    except sqlite3.OperationalError:
        pass  # Table doesn't exist, fall through
    finally:
        conn.close()
    return ["learner"]
```

### BUG-007: Test isolation — session-scoped DB accumulates data
- **File:** `tests/conftest.py` + `tests/test_learning_tracker.py`
- **Impact:** 7 tests in learning_tracker produce false failures (expected vs actual mismatches)
- **Root Cause:** `shared_db_path` is session-scoped — data from test class A pollutes test class B
- **Fix:** Change fixture scope or add per-test cleanup:
```python
@pytest.fixture(scope="function")  # Was implicitly session via shared_db_path
def learning_tracker_fixture(shared_db_path):
    from core.database import init_db
    init_db()
    from core.learning_tracker import LearningTracker
    return LearningTracker(db_path=shared_db_path)
```

---

## 🟡 Medium Bugs

### BUG-008: `init_audit_db()` runs on every module import
- **File:** `core/security.py`
- **Lines:** 33-34
- **Impact:** Creates empty `audit_log` table on every import of security.py
- **Root Cause:** Module-level function call `init_audit_db()` executes at import time
- **Fix:** Only call when explicitly needed; remove auto-init or guard with settings check

### BUG-009: Training effectiveness SQL template syntax
- **File:** `core/analytics.py`
- **Line:** 75
- **Impact:** `course_id` parameter is defined but never used (template syntax `{% if %}` is not valid Python/SQLite)
- **Root Cause:** SQL uses Jinja-like template syntax that isn't processed
- **Fix:** Remove unused `course_id` parameter or implement conditional SQL properly

### BUG-0010: Rate limiter uses in-memory dict — not persistent
- **File:** `core/security.py`
- **Lines:** 24-32
- **Impact:** Rate limiter state lost on server restart; also not distributed across processes
- **Root Cause:** `self.requests = defaultdict(list)` — purely in-memory
- **Fix:** For production, use Redis-backed rate limiter or database-backed

### BUG-0011: Middleware app state pollution between test modules
- **File:** `api/middleware.py` + multiple test files
- **Impact:** 3 middleware tests fail because TestClient shares app state across modules
- **Root Cause:** Each test module uses `from main import app` which caches the same app instance
- **Fix:** Use `TestClient(app, raise_server_exceptions=False)` consistently and reset app state between tests

### BUG-0012: Role validation missing in `RegisterRequest`
- **File:** `api/routes/auth.py`
- **Lines:** 15-16
- **Impact:** Any arbitrary string accepted as role (e.g., "admin", "superadmin", "godmode")
- **Root Cause:** No enum or validation on `role` field
- **Fix:**
```python
class RegisterRequest(BaseModel):
    ...
    role: str = Field(default="learner")
    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v not in ("admin", "trainer", "learner", "viewer"):
            raise ValueError("Role must be one of: admin, trainer, learner, viewer")
        return v
```

---

## 🟢 Low Bugs / Improvements

### BUG-0013: Health check checks `request.app.state.analyzer` but app sets `competency_analyzer`
- **File:** `api/routes/health.py`
- **Line:** 18
- **Impact:** Health check always returns `database: "unknown"` even when server is running
- **Root Cause:** Property name mismatch — `app.state.competency_analyzer` vs check for `app.state.analyzer`
- **Fix:** Change to `request.app.state.competency_analyzer` or `hasattr(request.app.state, 'competency_analyzer')`

### BUG-0014: `sanitize_llm_input` may over-trim legitimate text
- **File:** `core/security.py`
- **Lines:** 38-42
- **Impact:** Text containing "system" or "you are" as regular words gets stripped
- **Root Cause:** Simple regex replace without context awareness
- **Fix:** Use word boundary matching or more sophisticated prompt injection detection

### BUG-0015: File processor chunking timeout
- **File:** `tests/test_file_processor.py`
- **Impact:** Chunking tests timeout (60s limit)
- **Root Cause:** Large text chunking with overlap is O(n²) in worst case
- **Fix:** Optimize chunking algorithm or increase timeout; add unit test with smaller text

---

## 📊 Uncovered Backend Areas (No Tests)

The following backend modules have **zero test coverage**:

| Module | Purpose | Risk |
|--------|---------|------|
| `core/classifier.py` | Competency analysis using NLP | High |
| `core/rag.py` | Course recommendation via RAG | High |
| `core/virtual_assistant.py` | AI assistant for learners | High |
| `core/adaptive_quiz.py` | Adaptive difficulty quizzes | Medium |
| `core/embeddings.py` | Embedding generation | Medium |
| `api/routes/pipeline.py` | Full document processing pipeline | High |
| `api/routes/classify.py` | Profile classification endpoint | Medium |

These should be tested before production deployment.

---

## Fix Priority Matrix

| Priority | Bug IDs | Effort | Description |
|----------|---------|--------|-------------|
| P0 | BUG-001, BUG-002 | 30min | Fix missing fixtures — unblocks 33 tests |
| P0 | BUG-003 | 15min | Fix no-op RBAC decorator |
| P1 | BUG-004, BUG-005, BUG-006 | 1h | Fix crash bugs in scoring, JWT, auth |
| P1 | BUG-007 | 30min | Fix test isolation |
| P2 | BUG-008, BUG-009, BUG-010 | 1h | Code quality improvements |
| P2 | BUG-011 | 45min | Fix middleware test pollution |
| P2 | BUG-012 | 15min | Add role validation |
| P3 | BUG-013, BUG-014, BUG-015 | 30min | Minor fixes |
