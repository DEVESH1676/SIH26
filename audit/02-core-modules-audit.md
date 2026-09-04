# Part 2: Core Modules Deep Audit & Unit Test Results

## 1. `core/database.py` — Database Layer

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| Table Design | ✅ Good | All 11 tables properly defined with correct types |
| Security | ⚠️ Medium | Admin password stored with bcrypt — correct |
| Initialization | ✅ Good | `CREATE TABLE IF NOT EXISTS` prevents duplicate creation |
| Idempotent | ✅ Good | Admin user check prevents duplicate admin |
| Path Safety | ⚠️ Minor | `os.makedirs(os.path.dirname(...))` fails if path is root |

### Test Results: `test_database.py` — ✅ 14/14 PASS

All database tests passed:
- ✅ All 11 tables created correctly on init
- ✅ Users table schema verified (8 columns including `created_at`)
- ✅ Quiz questions, attempts, learning sessions, audit log schemas validated
- ✅ Default admin user (`admin`/`admin123`) created with hashed password
- ✅ Admin password not duplicated on multiple `init_db()` calls
- ✅ Data insertion and retrieval tested for `learner_progress`, `competency_scores`, `file_uploads`

### Issues Found
- **None in production code** — all 14 tests passed cleanly
- **Note:** `settings.sqlite_path` default is `"data/mospi_learning.db"` but conftest overrides to temp paths — this is fine

---

## 2. `core/auth.py` — Authentication Module

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| Password Hashing | ✅ Good | bcrypt with gensalt — industry standard |
| JWT Implementation | ✅ Good | pyjwt library, proper expiry handling |
| RBAC Model | ✅ Good | 4 roles: admin, trainer, learner, viewer with permission matrix |
| Token Decoding | ✅ Good | Silent failure on invalid tokens (not leaking info) |
| DB Access | ⚠️ Medium | `get_user_roles()` assumes `user_roles` table exists — crashes if not |
| Decorator | ❌ Bad | `require_role()` decorator is a no-op — does NOT enforce roles |

### Test Results: `test_auth.py` — ⚠️ 19/21 PASS, 2 FAIL

**Passed Tests (19):**
- ✅ Password hashing (format, salt, verification, unicode, empty)
- ✅ JWT creation and decoding (access tokens, refresh tokens, expiry)
- ✅ Token tampering detection
- ✅ RBAC role definitions and permission checks

**Failed Tests (2):**

#### FAIL 1: `test_refresh_token_longer_expiry`
```
AssertionError: assert (1789113204 - 1789113204) > 500000
```
- **Root Cause:** `create_refresh_token()` sets `exp` but the test expects `iat` (issued-at) field. The JWT payload lacks an `iat` claim, so `d.get("iat", d["exp"])` returns `exp`, giving a diff of 0.
- **Severity:** Medium — The JWT library auto-adds `iat` in newer versions but the test assumes explicit inclusion.
- **Fix:** Either add `iat` explicitly in `create_refresh_token()` or fix the test to not depend on `iat`.

#### FAIL 2: `test_check_permission`
```
sqlite3.OperationalError: no such table: user_roles
```
- **Root Cause:** `check_permission()` → `get_user_roles()` queries `user_roles` table which doesn't exist in the conftest shared DB (only `init_db()` from `database.py` creates it). The test uses `core/auth.py` in isolation without calling `database.init_db()`.
- **Severity:** Medium — Real bug. Any code path calling `check_permission()` without ensuring `user_roles` table exists will crash.
- **Fix:** Add `CREATE TABLE IF NOT EXISTS user_roles` in `get_user_roles()` or ensure all auth code paths call `init_db()` first.

---

## 3. `core/competency_framework.py` — Competency Framework

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| Data Structure | ✅ Good | 4 domains, 30+ competencies with proper schema |
| Search | ✅ Good | Case-insensitive, searches name/description/sub_competencies |
| Difficulty Levels | ✅ Good | beginner/intermediate/advanced per competency |
| Extensibility | ✅ Good | Easy to add new competencies |

### Test Results: `test_competency_framework.py` — ✅ 28/28 PASS

All tests passed:
- ✅ All 4 domains present (statistical, technical, digital_governance, behavioural)
- ✅ Competency counts: statistical ≥9, technical ≥10, digital_governance ≥3, behavioural ≥4
- ✅ All competencies have required fields (id, name, description, difficulty_levels)
- ✅ Difficulty levels properly structured (beginner/intermediate/advanced with lists)
- ✅ Search functionality (by name, case-insensitive, description, sub_competency, no results)
- ✅ Specific competency IDs validated (STAT-001, TECH-001, TECH-003, DG-001, BEH-004)

### Issues Found
- **None** — clean module with excellent test coverage

---

## 4. `core/quiz_engine.py` — Quiz Engine

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| Quiz Generation | ⚠️ Medium | LLM-dependent; fails gracefully if LLM unavailable |
| Scoring | ✅ Good | Handles string/numeric IDs, partial correctness |
| DB Tables | ✅ Good | Self-initializes quiz tables |
| Score Calculation | ❌ Bad | `calculate_score()` assumes `q["question"]` key exists — crashes if missing |
| JSON Parsing | ⚠️ Medium | LLM JSON output parsing is fragile (backtick stripping) |

### Test Results: `test_quiz_engine.py` — ⚠️ 16/17 PASS, 1 FAIL

**Passed Tests (16):**
- ✅ Quiz engine DB tables created (quizzes, quiz_questions, quiz_attempts)
- ✅ Custom DB path works
- ✅ Quiz retrieval (nonexistent, with questions, empty questions)
- ✅ Score calculation (all correct, all wrong, partial, pass threshold 60%, fail below 60%, empty, results detail, string IDs)
- ✅ LLM quiz generation returns proper dict structure

**Failed Test (1):**

#### FAIL: `test_score_with_string_keys`
```
KeyError: 'question'
```
- **Root Cause:** The test passes minimal question dicts `{"id": "1", "correct_answer": "0"}` but `calculate_score()` requires `q["question"]` key (line 230 in quiz_engine.py). The method should handle missing keys gracefully.
- **Severity:** High — This is a real production bug. If any quiz data is missing the `question` field, scoring will crash.
- **Fix:** Use `q.get("question", "")` instead of `q["question"]`.

---

## 5. `core/attempt_tracker.py` — Attempt Tracker

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| Data Model | ✅ Good | Records attempt_id, quiz_id, learner_id, answers, score, time |
| History Query | ✅ Good | JOINs with quizzes for title/difficulty, ordered by completion |
| Performance Analytics | ✅ Good | Aggregates: total_attempts, avg/best/worst scores, pass_rate, avg_time |
| Pass Threshold | ✅ Good | Hardcoded 60% in SQL CASE statement |
| Error Handling | ⚠️ Medium | No error handling — crashes if `quiz_attempts` table missing |

### Test Results: `test_attempt_tracker.py` — ❌ 0/13 PASS, 13 ERRORS

**All 13 tests failed** with `NameError: name 'shared_db_path' is not defined`

- **Root Cause:** Test file defines its own `_init_db` fixture but methods reference `shared_db_path` which is not in scope. The test file needs to import the fixture from `conftest.py` or use its own db path variable.
- **Severity:** Critical — Entire test suite is non-functional
- **Fix:** Rename the local fixture variable to match usage, or add `@pytest.fixture` decorator for `shared_db_path` in this file.

---

## 6. `core/analytics.py` — Learning Analytics

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| Admin Overview | ✅ Good | Counts learners, sessions, quizzes, courses |
| Workforce Competency | ✅ Good | Groups by competency, calculates avg_score and mastery_rate |
| Training Effectiveness | ⚠️ Medium | SQL has unused `course_id` parameter (template syntax `{% if %}` is not Jinja) |
| Predictive Needs | ✅ Good | Simple trend analysis — identifies 10% decline in scores |
| Data Dependencies | ⚠️ Medium | Requires `quiz_attempts`, `competency_scores`, `learner_progress` to have data |

### Test Results: `test_analytics.py` — ❌ 1/21 PASS, 20 ERRORS

**Only 1 test passed:** `test_empty_db_returns_empty_list` (created its own temp DB)

**All 20 other tests failed** with `fixture 'analytics_db' not found`

- **Root Cause:** Test references a non-existent `analytics_db` fixture. The conftest provides `shared_db_path`, not `analytics_db`. The test file needs a fixture that initializes the database and creates an `LearningAnalytics` instance.
- **Severity:** Critical — Entire test suite is non-functional
- **Fix:** Add fixture in conftest or test file:
  ```python
  @pytest.fixture
  def analytics_db(shared_db_path):
      from core.database import init_db
      init_db()
      # Create test data...
      return LearningAnalytics(db_path=shared_db_path)
  ```

---

## 7. `core/learning_tracker.py` — Learning Tracker

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| Activity Logging | ✅ Good | UUID-based session IDs, JSON metadata |
| Learning Hours | ✅ Good | Period filtering with `started_at >= cutoff` |
| Course Progress | ✅ Good | `INSERT OR REPLACE` for upsert, tracks completion timestamp |
| Dashboard | ✅ Good | Aggregates hours, progress, and competency scores |
| DB Isolation | ⚠️ Bad | `_init_db()` creates tables but does NOT call `database.init_db()` — tables may differ |

### Test Results: `test_learning_tracker.py` — ⚠️ 11/18 PASS, 7 FAIL

**Passed Tests (11):**
- ✅ Basic activity logging (with/without metadata)
- ✅ Empty learning hours, basic hours calculation
- ✅ Course progress (update, replace, complete flag, progress not complete)
- ✅ Empty dashboard, dashboard keys

**Failed Tests (7):**

All 7 failures are caused by **test isolation issues** — the session-scoped `shared_db_path` accumulates data from previous test runs:

| Test | Expected | Actual | Cause |
|------|----------|--------|-------|
| `test_log_activity_creates_records` | total_sessions == 2 | 5 | Stale data from prior tests |
| `test_total_hours_calculation` | total_hours == 1.0 | 1.15 | Extra data in DB |
| `test_multiple_sessions_hours` | total_hours == 1.5 | 2.65 | Accumulated sessions |
| `test_average_session_duration` | average == 2.5 | 16.4 | Stale session data |
| `test_period_filtering` | total_hours == 0.0 | 2.73 | Sessions not properly filtered |
| `test_multiple_courses_progress` | len == 2 | 3 | Old `course1` from prior test |
| `test_dashboard_with_data` | total_sessions == 1 | 13 | Massive data accumulation |

- **Root Cause:** The `learning_tracker_fixture` uses `shared_db_path` (session-scoped). Data from earlier test classes accumulates. The fixture should either use `function` scope or explicitly clean data.
- **Severity:** High — Tests produce false negatives
- **Fix:** Use `function`-scoped DB per test, or add cleanup logic in fixture.

---

## 8. `core/security.py` — Security Utilities

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| Rate Limiter | ✅ Good | Sliding window, per-key independent |
| Sanitization | ✅ Good | Removes system prompts, code blocks, truncates to 50K chars |
| Audit Logging | ✅ Good | JSON details, timestamps, per-action logging |
| DB Init | ⚠️ Medium | `init_audit_db()` runs on import — may create table before settings loaded |
| Auto-Init | ⚠️ Medium | `init_audit_db()` called at module level — runs on every import |

### Test Results: `test_security.py` — ✅ 19/19 PASS

All security tests passed:
- ✅ Rate limiter: allows within limit, blocks over limit, independent keys, window expiry
- ✅ Sanitization: normal text unchanged, system prompts removed, code blocks removed, truncation
- ✅ Audit log: creates entries, stores action/user_id/details
- ✅ Audit DB table exists

### Issues Found
- **None in production code** — all 19 tests passed cleanly
- **Minor:** `init_audit_db()` runs on import which may create empty tables before the real DB is configured

---

## 9. `core/file_processor.py` — File Processor

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| Text Processing | ✅ Good | Handles unicode, multiline, empty files |
| Extension Handling | ✅ Good | Case-insensitive, supports dot prefix |
| Chunking | ⚠️ Slow | Large text chunking may hang (test timed out at 60s) |
| PDF Support | ⚠️ Conditional | Requires `pypdf` — ImportError if missing |
| Error Handling | ✅ Good | Unsupported types raise ValueError with helpful message |

### Test Results: `test_file_processor.py` — ⏸️ Partial (timeout on chunking test)

**Passed Tests (14):**
- ✅ Upload dir creation (Pathlib, directory existence)
- ✅ TXT processing (simple, multiline, empty, unicode, case-insensitive, dot prefix)
- ✅ Unsupported types (xyz, html, image) raise ValueError with correct message

**Not Completed (5):**
- ⏸️ Chunking tests — timeout at 60s on `test_basic_chunking` (first chunking test)
- ⏸️ Missing dependencies test — not reached

---

## 10. `core/classifier.py`, `core/rag.py`, `core/virtual_assistant.py`, `core/adaptive_quiz.py`, `core/embeddings.py`

These modules were **not tested** by any test file. They are important backend components:

- **classifier.py** (CompetencyAnalyzer) — No tests
- **rag.py** (CourseRecommender) — No tests
- **virtual_assistant.py** — No tests
- **adaptive_quiz.py** — No tests
- **embeddings.py** — No tests
