# MoSPI AI Learning Platform — Migration Audit & Implementation Plan

> **Project**: Transform Nexus AI Ticket Intelligence Platform → MoSPI AI Skill Intelligence & Learning Platform  
> **Problem Statement**: SIH26 Problem 26101  
> **Stack**: FastAPI + React 19/Vite + SQLite + ChromaDB + Groq/Ollama + iGOT Karmayogi API

---

## Audit Structure

The migration is organized into **10 sequential parts** within this directory. Each part is a self-contained work package with file-level specifications.

| Part | Directory | Description | Status |
|------|-----------|-------------|--------|
| 1 | `part.1-gap-assessment/` | Gap assessment matrix, code-level flaws, risk register | ✅ Complete |
| 2 | `part.2-configuration-dependencies/` | `config.py` → `settings.py`, requirements cleanup, `.env` template | ✅ Complete |
| 3 | `part.3-core-competency-engine/` | Competency framework, `classifier.py`, `rag.py`, `agent.py` rebuild | ✅ Complete |
| 4 | `part.4-igot-integration/` | iGOT Karmayogi API client, NSSTA TPAC, course recommender, background sync | ✅ Complete |
| 5 | `part.5-file-processing-quiz-engine/` | PDF/DOCX/PPTX/video processing, MCQ generation, attempt tracking | ✅ Complete |
| 6 | `part.6-virtual-assistant-analytics/` | AI assistant, adaptive quizzes, learning hours, admin analytics | ✅ Complete |
| 7 | `part.7-authentication-security/` | JWT auth, RBAC, rate limiting, input sanitization, audit logging | ✅ Complete |
| 8 | `part.8-database-schema/` | Complete database schema, SQLAlchemy models, `init_db()` | ✅ Complete |
| 9 | `part.9-frontend-restructuring/` | React pages, i18n, Zustand stores, file upload, virtual assistant widget | ✅ Complete |
| 10 | `part.10-deployment-testing/` | Docker, CI/CD, testing, `.env.example`, final `main.py` | ✅ Complete |

---

## How to Use This Audit

### Execution Order
Execute the parts **in sequence** (1 → 10). Each part builds on the previous one.

```bash
# Step 1: Read the gap assessment
cat audits/update-v1/part.1-gap-assessment/CHANGELOG.md

# Step 2: Update configuration
cat audits/update-v1/part.2-configuration-dependencies/CHANGELOG.md

# ... continue through all 10 parts

# Step 10: Deploy and test
cat audits/update-v1/part.10-deployment-testing/CHANGELOG.md
```

### For Each Part
Every `CHANGELOG.md` contains:
- **File operations**: CREATE, UPDATE, or DELETE with exact code
- **Line-by-line changes**: What to add, remove, or modify
- **Verification checklist**: Items to confirm before moving to next part

### File Operation Legend
- `CREATE` = New file that doesn't exist yet
- `UPDATE` = Existing file that needs to be completely rewritten
- `DELETE` = Existing file that should be removed
- `MODIFY` = Partial changes to existing file

---

## Summary of Major Changes

### Architecture Shifts
1. **Domain**: IT ticket routing → Statistical competency learning
2. **Users**: Anonymous ticket submitters → Registered learners with roles
3. **Data**: Ticket embeddings → Course catalog, quiz questions, competency scores
4. **API**: Ticket classification → Course recommendation, quiz generation, progress tracking
5. **Frontend**: Ticket dashboard → Learning platform with multiple pages

### New Core Modules (14 files)
| File | Purpose |
|------|---------|
| `core/igot_api.py` | iGOT Karmayogi API client |
| `core/igot_sync.py` | Background catalog synchronization |
| `core/file_processor.py` | PDF/DOCX/PPTX/video text extraction |
| `core/quiz_engine.py` | LLM-based MCQ generation |
| `core/attempt_tracker.py` | Quiz attempt recording & analysis |
| `core/adaptive_quiz.py` | Adaptive difficulty quiz system |
| `core/learning_tracker.py` | Learning hours & progress tracking |
| `core/analytics.py` | Admin analytics engine |
| `core/virtual_assistant.py` | AI-powered learning assistant |
| `core/auth.py` | JWT authentication & password hashing |
| `core/security.py` | Rate limiting, sanitization, audit |
| `core/database.py` | Database initialization & schema |
| `config/settings.py` | Pydantic-based configuration |
| `api/middleware.py` | Auth, RBAC, CORS, rate-limit middleware |

### New API Routes (4 files)
| Route | Description |
|-------|-------------|
| `api/routes/auth.py` | Login, register, refresh, profile |
| `api/routes/assessment.py` | Quiz generation & scoring |
| `api/routes/classify.py` | Competency analysis |
| `api/routes/pipeline.py` | Course recommendation pipeline |

### Frontend Pages (6 new)
| Page | Replaces |
|------|----------|
| `pages/Login.tsx` | N/A (new) |
| `pages/Dashboard.tsx` | `Pages/Blueprint.tsx` |
| `pages/Courses.tsx` | `Pages/Operations.tsx` |
| `pages/QuizTake.tsx` | N/A (new) |
| `pages/Analytics.tsx` | `Analytics/AnalyticsMock.tsx` |
| `pages/AdminPanel.tsx` | N/A (new) |

---

## Risk Register (from Part 1)

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| 1 | iGOT API unavailable/unstable | 🔴 High | Graceful degradation with cached data |
| 2 | PII data under DPDP Act | 🔴 High | Encryption at rest, RBAC, audit logging |
| 3 | LLM rate limits / costs | 🟡 Medium | Ollama fallback, request batching |
| 4 | Large file processing timeouts | 🟡 Medium | Chunking, background processing |
| 5 | ChromaDB migration complexity | 🟡 Medium | Parallel schema, rollback plan |
| 6 | Multi-language quality | 🟢 Low | Start with English + Hindi |
| 7 | Video transcription accuracy | 🟢 Low | Use Whisper model, allow manual review |
| 8 | Frontend performance with analytics | 🟢 Low | Pagination, lazy loading, recharts |
| 9 | Container image size | 🟢 Low | Multi-stage Docker build |
| 10 | Government compliance review | 🟢 Low | Early engagement with MoSPI IT team |

---

## Implementation Strategy

### Phase 1: Foundation (Parts 1-3)
- Gap analysis complete
- Configuration overhaul
- Core competency engine rebuilt

### Phase 2: Integration (Parts 4-6)
- iGOT API integration
- File processing & quiz generation
- Analytics & virtual assistant

### Phase 3: Security (Part 7)
- Authentication & authorization
- Rate limiting & sanitization
- Audit logging

### Phase 4: Persistence (Part 8)
- Database schema migration
- SQLAlchemy models
- Initialization scripts

### Phase 5: Frontend (Part 9)
- Complete React rewrite
- i18n multi-language
- Role-based dashboards

### Phase 6: Deployment (Part 10)
- Docker containerization
- CI/CD pipeline
- Testing & validation

---

## Quick Start (After Implementation)

```bash
# 1. Setup
cp .env.example .env  # Edit with your keys
pip install -r requirements.txt

# 2. Initialize database
python -c "from core.database import init_db; init_db()"

# 3. Start backend
uvicorn main:app --reload --port 8000

# 4. Start frontend
cd frontend-v2 && npm run dev

# 5. Run tests
pytest tests/ -v
```

---

## Files to Delete

After migration, remove these IT-ticket-specific files:
- `scripts/calibrate.py`
- `scripts/ingest_kaggle.py`
- `core/judge.py`
- `core/embeddings.py` (replaced by iGOT sync)
- `core/feedback.py` (replaced by attempt tracker)
- `frontend-v2/src/hooks/usePipeline.tsx`
- All IT-ticket-specific datasets and CSVs

## Files to Archive (potentially reusable)
- `shadcn/ui` components (keep, refactor for new domain)
- `components/Command/GlowingProgressBar.tsx` (keep for loading states)
- LLM calling patterns in `core/rag.py` (reuse, refactor for learning domain)

---

*Generated for SIH26 Problem 26101 — MoSPI AI Skill Intelligence & Learning Platform*
