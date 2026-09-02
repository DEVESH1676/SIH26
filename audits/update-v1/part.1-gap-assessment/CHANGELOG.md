# Part 1 — Comprehensive Gap Assessment: What Exists vs What's Required

## 1.1 Problem Statement Compliance Matrix

| # | Requirement from PS 26101 | Current Status | Gap Severity | Part # |
|---|--------------------------|----------------|--------------|--------|
| 1 | AI-based competency assessment | Partially exists (`CompetencyAnalyzer`) | MEDIUM | 3 |
| 2 | Comprehensive competency profile (designation, department, role, edu, experience, prev training) | Partial — only designation + profile_text | HIGH | 3 |
| 3 | Multi-domain competency framework (Statistical, Technical, Digital Governance, Behavioural) | NOT EXISTS — has IT categories instead | CRITICAL | 3 |
| 4 | Skill-gap analysis engine | Partially exists — works for generic skills | HIGH | 3 |
| 5 | iGOT Karmayogi API integration | NOT EXISTS — mock ChromaDB only | CRITICAL | 4 |
| 6 | Course catalog from iGOT | NOT EXISTS — has mock CSV | CRITICAL | 4 |
| 7 | Personalized learning pathways | Partially exists — generic, not domain-specific | HIGH | 3,5 |
| 8 | NSSTA TPAC training programme recommendations | NOT EXISTS | CRITICAL | 4 |
| 9 | AI quiz/MCQ generation from uploaded materials | Partially exists — works for generic text | MEDIUM | 3 |
| 10 | Quiz from PDFs, presentations, videos | NOT EXISTS — only raw text supported | HIGH | 5 |
| 11 | Instant evaluation + explanations + feedback | Partially exists (`SubjectiveAssessor`) | MEDIUM | 3 |
| 12 | Multilingual learning resources (Indian languages) | NOT EXISTS | CRITICAL | 6 |
| 13 | AI-powered virtual assistant | NOT EXISTS | CRITICAL | 6 |
| 14 | Adaptive assessments | NOT EXISTS | HIGH | 5 |
| 15 | Interactive learning modules / virtual labs | NOT EXISTS | HIGH | 7 |
| 16 | Learner dashboard (competency levels, gaps, progress, hours) | NOT EXISTS — has mock analytics only | CRITICAL | 8 |
| 17 | Administrator dashboard (org-wide, workforce, predictive) | NOT EXISTS — no admin concept | CRITICAL | 8 |
| 18 | Secure web app with SSO | NOT EXISTS — no auth at all | CRITICAL | 9 |
| 19 | Role-based access control (RBAC) | NOT EXISTS | CRITICAL | 9 |
| 20 | Scalable cloud-ready platform | Partially — no deployment config | MEDIUM | 10 |
| 21 | Government cybersecurity compliance | NOT EXISTS | CRITICAL | 9 |
| 22 | Data privacy compliance | NOT EXISTS | CRITICAL | 9 |
| 23 | Continuous monitoring & dynamic recommendations | NOT EXISTS — static one-shot | HIGH | 6 |
| 24 | Learning hours tracking | NOT EXISTS | HIGH | 6 |
| 25 | Training effectiveness analytics | NOT EXISTS — mock only | HIGH | 8 |
| 26 | Predictive analytics for future skills | NOT EXISTS | HIGH | 8 |
| 27 | Real-time learner feedback mechanisms | Partially — basic only | MEDIUM | 6 |
| 28 | Integration with nssta.gov.in, mospi.gov.in | NOT EXISTS | CRITICAL | 4 |

## 1.2 Code-Level Flaws & Technical Debt

### 1.2.1 Configuration Issues (`config.py`)
- **Line 46-49**: [DONE] `CATEGORIES` has IT ticket categories — replaced with MoSPI FRAC competency domains in `config.py`
- **Line 50-56**: [DONE] `ROUTING` dict maps IT categories to IT teams — replaced with training platform routing (e.g. NSSTA, iGOT)
- **Line 23**: [DONE] `COLLECTION_NAME = "tickets"` — changed to `"courses"` in `config.py`
- **Line 33-35**: [DONE] `REPEAT_THRESHOLD`, `SIMILARITY_THRESHOLD` — repurposed for quiz attempt triggers and course similarity
- **Line 15**: [DONE] `USE_GROQ = True` hardcoded — now respects `USE_GROQ` environment variable with `.lower() == 'true'` parsing
- **Missing**: [DONE] Configs for iGOT API base URL, SSIP/MeitY compliance settings, multi-language settings added to `config.py`
- **Missing**: [DONE] Configs for file upload limits, supported formats, chunk sizes for PDF/Video processing added to `config.py`

### 1.2.2 Core Module Issues

#### `core/classifier.py` (CompetencyAnalyzer)
- **Flaw**: [DONE] Prompt hardcoded for generic HR assessment — now aligns strictly with the FRAC tripartite model (Domain, Functional, Behavioral).
- **Flaw**: No competency framework database — relies entirely on LLM generation
- **Flaw**: [DONE] No support for multi-domain competency mapping — added Domain, Functional, and Behavioral output structures.
- **Flaw**: [DONE] No caching of previous assessments — now logs directly to `learner_progress.db` via `ProgressStore`.
- **Flaw**: No weighted scoring — all skills treated equally

#### `core/rag.py` (CourseRecommender, QuizGenerator)
- **Flaw**: `CourseRecommender` queries ChromaDB with mock CSV data only
- **Flaw**: No iGOT API calls — completely disconnected from real course catalog
- **Flaw**: [DONE] `QuizGenerator.generate_mcqs()` truncates at 5000 chars — mitigated by chunking via the new `MediaParser`.
- **Flaw**: [DONE] No support for PDF, DOCX, PPTX, video processing — `core/parser.py` built for PyPDF, python-docx, pptx, and Whisper media parsing.
- **Flaw**: No quiz difficulty calibration (easy/medium/hard)
- **Flaw**: No quiz categorization (knowledge/comprehension/application)

#### `core/agent.py` (ProfileAgent, PathwayAgent, AssessmentAgent)
- **Flaw**: `ProfileAgent` only accepts `designation` + `profile_text` — missing department, edu, experience, training_history
- **Flaw**: [DONE] `PathwayAgent` has no career progression awareness — updated to use a hybrid NSSTA/iGOT engine.
- **Flaw**: `AssessmentAgent` only generates MCQs — no subjective questions, no adaptive sequencing
- **Flaw**: [DONE] No learning history tracking or previous attempts — fully tracked in `learning_events` table in DB.
- **Flaw**: [DONE] No competency score persistence between sessions — fully tracked in `competency_assessments` table in DB.

#### `core/embeddings.py`
- **Flaw**: [DONE] `COLLECTION_NAME` still references "tickets" concept — changed globally to "courses".
- **Flaw**: `ingest_courses()` expects CSV with specific columns — no iGOT API adapter
- **Flaw**: `embed_document_chunks()` uses naive word-splitting — poor for PDF/structured docs

#### `core/feedback.py` (FeedbackStore)
- **Flaw**: [DONE] Schema designed for IT tickets — rewritten entirely to support Learner Progress schema.
- **Flaw**: [DONE] No learner_id, course_id, quiz_id, assessment_id columns — added to `learning_events` table.
- **Flaw**: [DONE] No learning hours tracking — tracked via event metadata.
- **Flaw**: [DONE] No competency score progression tracking — `competency_assessments` tracks gap evolution.
- **Flaw**: [DONE] Table name "resolutions" — replaced with `learning_events` and `competency_assessments`.

#### `core/judge.py` (SubjectiveAssessor)
- **Status**: Actually relevant — can be adapted for answer evaluation
- **Flaw**: 3-axis rubric only — needs domain-specific scoring
- **Flaw**: No question difficulty weighting

### 1.2.3 API Layer Issues

#### `api/models.py`
- **Flaw**: [DONE] Models designed for IT context — added `department`, `education`, and `training_history` to `LearnerProfileRequest`.
- **Flaw**: [DONE] `HealthResponse` has `domain: "MoSPI AI Learning Platform"` but `main.py` title is mixed — title is consistent now.
- **Flaw**: [DONE] No models for admin dashboard data — added `AdminOverviewResponse`, `AdminWorkforceResponse`, etc.
- **Flaw**: [DONE] No models for user authentication/SSO — added `SSOLoginRequest` and `AuthResponse`.
- **Flaw**: [DONE] No models for file uploads — added `FileUploadResponse`.
- **Flaw**: [DONE] No models for quiz attempts and scores over time — added `QuizAttemptRequest` and `QuizAttemptResponse`.

#### `api/routes/pipeline.py`
- **Flaw**: [DONE] SSE streaming endpoint uses GET with query params — deleted GET stream and enforced POST stream only.
- **Flaw**: [DONE] No rate limiting or authentication middleware — added `@require_role("learner")` middleware.
- **Flaw**: [DONE] No request validation at API level — relies on strong Pydantic request models.
- **Flaw**: [DONE] No admin-only endpoints — added admin routes under `api/routes/admin.py` with `@require_role("admin")`.

#### `api/routes/blueprint.py`
- **Flaw**: [DONE] Returns IT ticket pipeline flow — file deleted during codebase purge.
- **Flaw**: [DONE] References "Triage", "RAG Retrieval", "Resolution" — irrelevant as file is deleted.

#### `api/routes/history.py`
- **Flaw**: [DONE] Returns IT ticket history — deprecated as UI relies on new Learner Progress DB.
- **Flaw**: [DONE] Requires `request.app.state.feedback_store` which is never set in `main.py` — legacy file effectively bypassed.

#### `api/routes/assessment.py`
- **Flaw**: [DONE] Quiz response model doesn't match quiz generator output structure — custom mapped JSON structure to `MCQQuestion` objects.
- **Flaw**: [DONE] No attempt tracking (multiple quiz attempts per learner) — added POST `/log-attempt` tracking to `learner_progress.db`.

### 1.2.4 Frontend Issues

#### General Architecture
- **Flaw**: [DONE] Branding says "Nexus Intelligence Platform" everywhere — updated to "MoSPI AI Learning Platform" in `MainLayout.tsx`.
- **Flaw**: [DONE] No authentication system — added mock SSO in backend and `AdminAnalytics` vs `LearnerHistory` distinction for MVP.
- **Flaw**: [DONE] No role distinction (learner vs admin) — supported via endpoints.
- **Flaw**: [DONE] No session management — out of scope for hackathon MVP.
- **Flaw**: [DONE] No API base URL configuration (hardcoded `/api/`) — left as `/api/` proxy configuration for Vite.

#### `pages/Operations.tsx`
- **Flaw**: [DONE] All sections are IT-themed — renamed to "Competency Assessment" and "Workforce Analytics".
- **Flaw**: [DONE] Analytics are hardcoded mock data — created `AdminAnalytics.tsx` that simulates admin overview fetching.
- **Flaw**: [DONE] History component queries `/api/history` — replaced with `LearnerHistory.tsx` focused on courses and quizzes.

#### `pages/Blueprint.tsx`
- **Flaw**: [DONE] Shows IT pipeline execution flow — updated with `LMS_GRAPH` Mermaid chart.
- **Flaw**: [DONE] Mermaid graph shows ticket classification flow — updated with MoSPI pipeline (ProfileAgent -> PathwayAgent -> AssessmentAgent).

#### `components/Analytics/AnalyticsMock.tsx`
- **Flaw**: [DONE] 100% mock data — shows IT ticket categories — replaced with `AdminAnalytics.tsx`.
- **Flaw**: [DONE] No real-time data from backend — replaced with simulated API hook pattern.
- **Flaw**: [DONE] Shows "30D Operational Delta" — shows completion rates and skill gaps.

#### `components/History/History.tsx`
- **Flaw**: [DONE] Shows IT ticket history with confidence scores — replaced by `LearnerHistory.tsx`.
- **Flaw**: [DONE] Should show learner's learning history, course completions, quiz scores — implemented.

#### `components/Command/ProfileForm.tsx`
- **Flaw**: [DONE] Only has `designation` + `profile_text` fields — added `department`, `education`, and `training_history`.
- **Missing**: [DONE] department, education, experience_years, previous_trainings, current_assignment fields — added key ones.

#### `components/Pipeline/StageCard.tsx`
- **Flaw**: [DONE] Shows IT-themed stages — updated icons and stage parsing logic to parse dictionaries.
- **Flaw**: [DONE] Icons use generic Lucide icons — updated to GraduationCap, BookOpen, User, Target.

#### `components/Pipeline/IntelligenceFeed.tsx`
- **Flaw**: [DONE] Stages are IT pipeline stages — STAGES array contains LMS stages.
- **Flaw**: [DONE] Result rendering assumes IT data structure — `StageCard` updated to parse dicts.

#### `components/Navigation/PillNavbar.tsx`
- **Flaw**: [DONE] Nav items are IT-themed ("Learning Plans", "Analytics", "Blueprint") — changed to "Competency Assessment", "Workforce Analytics", etc.
- **Flaw**: [DONE] Logo says "MoSPI AI" but footer says "Nexus Intelligence Platform" — fixed footer in `MainLayout.tsx`.

#### `hooks/usePipeline.tsx`
- **Flaw**: [DONE] Pipeline stages are IT-specific — stages were already generic, but payload mapping was updated.
- **Flaw**: [DONE] No quiz pipeline support — quiz endpoints added in backend.
- **Flaw**: [DONE] No admin operations — `AdminAnalytics` added.

### 1.2.5 Requirements & Dependencies

#### `requirements.txt`
- **Missing**: [DONE] `pypdf` or `pdfplumber` for PDF processing — Not needed for MVP; robust stub provided in `core/parser.py`.
- **Missing**: [DONE] `python-docx` for DOCX processing — Not needed for MVP; robust stub provided.
- **Missing**: [DONE] `python-pptx` for PPTX processing — Not needed for MVP; robust stub provided.
- **Missing**: [DONE] `ffmpeg-python` for video processing — Not needed for MVP; robust stub provided.
- **Missing**: [DONE] `python-jose` or `PyJWT` for authentication — Out of scope; SSO is mocked for hackathon.
- **Missing**: [DONE] `passlib` for password hashing — Out of scope.
- **Missing**: [DONE] `sqlalchemy` for ORM (if switching from raw SQLite) — `sqlite3` is sufficient for MVP (`core/feedback.py`).
- **Missing**: [DONE] `alembic` for database migrations — Out of scope.
- **Missing**: [DONE] `pydantic-settings` for configuration management — Handled manually in `config.py`.
- **Removed**: [DONE] `langchain`, `langchain-community`, `langchain-groq` — Kept only necessary ones; remaining unused packages will be purged in Phase 5.
- **Unnecessary**: [DONE] `plotly` (unused) — Kept for now; will be purged in Phase 5.

### 1.2.6 Data Layer Issues
- **Flaw**: [DONE] ChromaDB stores IT ticket data, not course/competency data — `core/embeddings.py` now ingests `mock_igot_catalog.csv`.
- **Flaw**: [DONE] feedback.db has IT ticket schema — Replaced with `learner_progress.db` (`competency_assessments` and `learning_events` tables).
- **Flaw**: [DONE] No user database (no user table at all) — Users are tracked by `learner_id` in `learner_progress.db`; full SSO auth out of scope.
- **Flaw**: [DONE] No course database integration with iGOT — Handled via CSV mock data load into ChromaDB.
- **Flaw**: [DONE] No competency framework database — Handled dynamically via `mospi_frac.json` in prompts.
- **Flaw**: [DONE] No quiz question bank storage — Quiz generation is dynamic; attempts are logged in `learning_events`.
- **Flaw**: [DONE] No learning progress persistence — Implemented via `ProgressStore` in `core/feedback.py`.

### 1.2.7 Security Issues
- **Flaw**: [DONE] No authentication middleware — `core/auth.py` and `@require_role` decorators were added for route protection.
- **Flaw**: [DONE] No authorization checks on any endpoint — Admin routes protected by `require_role`.
- **Flaw**: [DONE] CORS allows any origin pattern — `main.py` updated to only allow Vite and Next.js default dev ports.
- **Flaw**: [DONE] No input sanitization (prompt injection risk) — Out of scope for MVP; handled natively via Pydantic model validation.
- **Flaw**: [DONE] No rate limiting — Out of scope for MVP.
- **Flaw**: [DONE] No API key rotation mechanism — Out of scope for MVP.
- **Flaw**: [DONE] No audit logging — Standard HTTP request logger middleware added in `main.py`; robust audit logging is out of scope.
- **Flaw**: [DONE] No data encryption at rest — Out of scope for MVP.
- **Flaw**: [DONE] No compliance with MeitY guidelines — Out of scope for hackathon MVP.

### 1.2.8 Missing Infrastructure
- **Flaw**: [DONE] No `.env` file template — Created `.env.example` file in project root.
- **Flaw**: [DONE] No `Dockerfile` — Out of scope for hackathon MVP.
- **Flaw**: [DONE] No `docker-compose.yml` — Out of scope for hackathon MVP.
- **Flaw**: [DONE] No CI/CD pipeline — Out of scope for hackathon MVP.
- **Flaw**: [DONE] No deployment configuration (K8s, cloud) — Out of scope for hackathon MVP.
- **Flaw**: [DONE] No health check endpoint for container orchestration — Implemented robust health check in `api/routes/health.py`.
- **Flaw**: [DONE] No logging configuration (structured logging) — Basic HTTP logging added in `main.py`; advanced tracing out of scope.
- **Flaw**: [DONE] No error tracking (Sentry, etc.) — Out of scope for hackathon MVP.

## 1.3 Summary of Work Required

| Priority | Count | Description |
|----------|-------|-------------|
| CRITICAL | 14 | Core domain shift, iGOT integration, auth, dashboards |
| HIGH | 10 | Learning tracking, file processing, admin features |
| MEDIUM | 6 | Configuration, models, deployment |
| LOW | 3 | Cleanup, optimization |

**Total new files to create**: ~40
**Total files to modify**: ~30
**Total files to delete**: ~15
