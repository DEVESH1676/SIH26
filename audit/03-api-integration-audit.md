# Part 3: API Integration & Middleware Audit

## 1. `api/routes/` — API Endpoints

### Routes Overview

| Route | File | Method | Description | Test Coverage |
|-------|------|--------|-------------|---------------|
| `/api/health` | health.py | GET | Health check, DB status | ✅ (2 tests pass) |
| `/api/auth/register` | auth.py | POST | User registration | ✅ (7 tests pass) |
| `/api/auth/login` | auth.py | POST | User login | ✅ (3 tests pass) |
| `/api/auth/refresh` | auth.py | POST | Refresh access token | ✅ (3 tests pass) |
| `/api/auth/me` | auth.py | GET | Get current user | ✅ (2 tests pass) |
| `/api/analyze-profile` | classify.py | POST | Competency classification | ⚠️ (401 without auth) |
| `/api/pipeline/` | pipeline.py | POST | Full pipeline processing | ❌ No tests |
| `/api/admin/` | — | GET | Admin dashboard | ⚠️ (blocked by RBAC) |
| `/api/analytics/admin/` | — | GET | Analytics admin | ⚠️ (blocked by RBAC) |

### `api/routes/auth.py` — Authentication Routes

#### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| Input Validation | ✅ Good | Pydantic models with min_length, max_length constraints |
| Duplicate Detection | ✅ Good | Checks both username AND email |
| Password Storage | ✅ Good | bcrypt hashing via `core.auth.hash_password()` |
| JWT Issuance | ✅ Good | Separate access (1h) and refresh (7d) tokens |
| Refresh Token Validation | ✅ Good | Checks `type == "refresh"` claim |
| Error Messages | ⚠️ Medium | Generic "Invalid credentials" (good for security) |
| Role Handling | ⚠️ Medium | Role stored as single string in DB, split on `","` |

#### Test Results: `test_api_routes.py` — ✅ 18/19 PASS, 1 FAIL

**Passed Tests (18):**
- ✅ Health endpoint returns 200 with `status: "ok"`, has `version` and `database` keys
- ✅ Health response is JSON
- ✅ Register new user → 200 with `message` and `user_id`
- ✅ Register duplicate username → 409
- ✅ Register duplicate email → 409
- ✅ Register short username (2 chars) → 422
- ✅ Register short password (<8 chars) → 422
- ✅ Register missing fields → 422
- ✅ Login with registered user → 200 with access_token, refresh_token, token_type=bearer
- ✅ Login wrong password → 401
- ✅ Login nonexistent user → 401
- ✅ Get /me unauthenticated → 401
- ✅ Get /me authenticated → 200 with username, email, roles
- ✅ Refresh token endpoint → 200 with new access_token
- ✅ Refresh with access token → 401
- ✅ No auth header on refresh → 401
- ✅ Admin login works → 200 with access_token
- ✅ Admin can access /me endpoint

**Failed Test (1):**

#### FAIL: `test_default_admin_exists`
```
sqlite3.OperationalError: no such table: users
```
- **Root Cause:** Test directly queries the settings.sqlite_path but the test's `set_test_env` fixture creates a new temp DB, runs `init_db()`, then other tests run. By the time this test runs, the DB path has been reset to a new temp path by the autouse fixture.
- **Severity:** Medium — Test isolation issue
- **Fix:** The test should use the temp DB path from the fixture, not `get_settings().sqlite_path`.

---

## 2. `api/middleware.py` — Middleware Stack

### Middleware Order (outer to inner)
```
1. CORS (fastapi.middleware.cors)
2. Rate Limiting (custom)
3. Auth (custom) — skips /api/health, /api/auth/*, /docs, /openapi.json
4. RBAC (custom) — checks admin paths for view_analytics permission
5. Audit Logging (custom) — logs method, path, status, duration, user
```

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| CORS | ✅ Good | Configurable origins from settings |
| Auth Middleware | ✅ Good | Proper Bearer token parsing, skips public paths |
| RBAC Middleware | ✅ Good | Checks admin path prefixes, denies without view_analytics |
| Rate Limiting | ✅ Good | Uses core.security.RateLimiter (60 req/min default) |
| Audit Logging | ✅ Good | Logs per-request with timing info |
| Error Handling | ⚠️ Medium | Auth middleware doesn't handle malformed tokens gracefully in some paths |
| Public Path List | ⚠️ Medium | Hardcoded list may miss new public endpoints |

### Test Results: `test_middleware.py` — ⚠️ 13/16 PASS, 3 FAIL

**Passed Tests (13):**
- ✅ CORS is configured (origins list populated)
- ✅ Public health endpoint accessible (200)
- ✅ Docs and openapi.json accessible without auth
- ✅ Unauthenticated /api/auth/me → 401
- ✅ Missing auth header on /api/analyze-profile → 401
- ✅ Invalid token → 401
- ✅ Rate limiter blocks after limit
- ✅ Rate limit config present (rate_limit_per_minute > 0)
- ✅ Audit middleware exists
- ✅ Request logging configured
- ✅ Various auth middleware path checks

**Failed Tests (3):**

#### FAIL 1: `test_public_auth_endpoints_accessible`
```
sqlite3.OperationalError: no such table: users
```
- **Root Cause:** The test sends a login request to a non-existent user, which hits the auth route. The auth route tries to query `users` table, but the test's temp DB may not have `init_db()` called properly in the middleware test's fixture scope.
- **Severity:** High — Middleware tests depend on DB state from other tests

#### FAIL 2: `test_register_accessible`
```
sqlite3.OperationalError: no such table: users
```
- **Root Cause:** Same as above — the `set_test_env` fixture in this file calls `init_db()` but the TestClient reuses app state from previous test modules where the DB was different.
- **Severity:** High — App-level state pollution between test modules

#### FAIL 3: `test_learner_cannot_access_admin`
```
sqlite3.OperationalError: no such table: users
```
- **Root Cause:** Same pattern — registration fails because `users` table not found in the shared test DB context.
- **Severity:** High — RBAC test cannot execute

---

## 3. `api/models.py` — Pydantic Models

### Code Review
| Aspect | Rating | Notes |
|--------|--------|-------|
| HealthResponse | ✅ Good | Proper typed response model |
| RegisterRequest | ✅ Good | Validation constraints (min/max length) |
| LoginRequest | ✅ Good | min_length=3 for username, min_length=8 for password |
| Role Validation | ⚠️ Medium | Role accepted as any string — should validate against ROLES |

### Test Results: No dedicated test file exists

---

## 4. `api/deps.py` — Dependencies

No test coverage for dependency injection layer.

---

## Integration Test Gaps

The following areas have **no test coverage at all**:
1. **Pipeline endpoints** (`/api/pipeline/*`) — Full document processing pipeline
2. **Classify endpoints** (`/api/analyze-profile`) — Competency classification
3. **Admin endpoints** — Dashboard data, user management
4. **Analytics endpoints** — Organization-wide reports
5. **File upload/download** — `POST /api/upload`, file serving
6. **Concurrent requests** — No load testing
7. **CORS preflight** — No OPTIONS request testing
8. **Rate limit exhaustion** — Only simulated with RateLimiter class, not via HTTP
