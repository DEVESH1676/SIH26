# MoSPI AI Learning Platform — Backend API

> **AI-powered learning, assessment & skill-gap analysis engine** for government officials under the Ministry of Statistics and Programme Implementation (MoSPI), India. Integrated with **iGOT Karmayogi** and **NSSTA TPAC** course catalogs.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [Database](#database)
- [API Endpoints](#api-endpoints)
- [Core Services](#core-services)
- [Authentication & Authorization](#authentication--authorization)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Troubleshooting](#troubleshooting)

---

## Overview

This backend is a **FastAPI** application that provides:

| Feature | Description |
|---|---|
| **Competency Analysis** | Analyzes official profiles against the MoSPI Competency Framework to identify skill gaps |
| **Course Recommendations** | Recommends personalized learning pathways from iGOT/NSSTA catalogs using RAG |
| **Quiz Engine** | Auto-generates MCQs/adaptive quizzes from learning materials (PDF, DOCX, PPTX, XLSX) |
| **Learning Tracking** | Tracks sessions, progress, and competency scores over time |
| **Admin Analytics** | Workforce competency dashboards, training effectiveness, and predictive gap analysis |
| **Virtual Assistant** | AI chatbot with intent detection and resource suggestions |
| **File Upload & Processing** | Extract text from documents and auto-generate quizzes |

---

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│   Frontend   │────▶│   FastAPI Server  │────▶│   SQLite     │
│  (React/Vite) │◀────│  (main.py:8000)  │◀────│  (mospi.db)  │
└─────────────┘     └────────┬─────────┘     └──────────────┘
                             │
                    ┌────────▼─────────┐
                    │   ChromaDB       │
                    │  (Vector Store)   │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐     ┌──────────────┐
                    │  LLM Provider    │────▶│  Groq API    │
                    │  (Groq or Ollama)│────▶│  (Cloud LLM)  │
                    └──────────────────┘     └──────────────┘
```

### Tech Stack

| Layer | Technology |
|---|---|
| **Web Framework** | FastAPI 0.135+ with Uvicorn |
| **Database** | SQLite 3 (SQLAlchemy ORM + raw SQL) |
| **Vector DB** | ChromaDB (semantic search over courses) |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2 / nomic-embed-text) |
| **LLM** | Groq (cloud) or Ollama (local) |
| **Auth** | JWT (python-jose) + bcrypt |
| **File Parsing** | pypdf, python-docx, python-pptx, openpyxl |
| **Analytics** | pandas, numpy |
| **Testing** | pytest + pytest-asyncio + httpx |

---

## Project Structure

```
├── main.py                  # Application entry point & lifespan
├── requirements.txt         # Python dependencies
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yml       # Docker orchestration
├── nginx.conf               # Nginx reverse proxy config
├── config/
│   └── settings.py          # Pydantic Settings (env-driven)
├── core/
│   ├── agent.py             # AI agent orchestration
│   ├── analytics.py         # Admin analytics engine
│   ├── attempt_tracker.py   # Quiz attempt recording
│   ├── auth.py              # JWT auth, password hashing, RBAC
│   ├── classifier.py        # Competency analysis engine
│   ├── competency_framework.py  # MoSPI competency definitions
│   ├── database.py          # SQLite schema & init
│   ├── embeddings.py        # Embedding model & ChromaDB setup
│   ├── file_processor.py    # PDF/DOCX/PPTX/XLSX text extraction
│   ├── learning_tracker.py  # Session & progress tracking
│   ├── quiz_engine.py       # Quiz generation & scoring
│   ├── rag.py               # RAG-based course recommendation
│   ├── security.py          # Rate limiter, security utilities
│   ├── virtual_assistant.py # AI chatbot
│   └── adaptive_quiz.py     # Adaptive quiz engine
├── api/
│   ├── models.py            # Pydantic request/response schemas
│   ├── middleware.py        # CORS, auth, RBAC, rate-limit, audit
│   ├── deps.py              # Dependency injection helpers
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # POST /login, /register, /refresh, /me
│       ├── classify.py      # POST /analyze-profile
│       ├── health.py        # GET /health
│       └── pipeline.py      # POST /generate-plan, /stream (SSE)
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_auth.py
│   ├── test_database.py
│   ├── test_quiz_engine.py
│   ├── test_competency_framework.py
│   ├── test_file_processor.py
│   ├── test_learning_tracker.py
│   ├── test_attempt_tracker.py
│   ├── test_analytics.py
│   ├── test_middleware.py
│   └── test_api_routes.py
└── data/
    ├── mospi_learning.db    # SQLite database (auto-created)
    ├── chroma/              # ChromaDB persistent store
    └── uploads/             # Uploaded files
```

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| **Python** | 3.12+ | Required for type-annotation features |
| **pip / venv** | latest | For virtual environment setup |
| **Node.js** | 18+ (optional) | Only if building frontend |
| **Docker** | 24+ (optional) | For containerized deployment |
| **Docker Compose** | 2.20+ | For stack orchestration |
| **Ollama** | latest (optional) | For local LLM inference |
| **Groq API Key** | — | For cloud LLM (alternative to Ollama) |

---

## Installation

### 1. Clone & Navigate

```bash
cd /home/devesh/Projects/SIH26
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **fastapi[standard]** — Web framework + dev server
- **uvicorn[standard]** — ASGI server
- **sqlalchemy + alembic + aiosqlite** — Database layer
- **chromadb + sentence-transformers** — Vector search & embeddings
- **python-jose + passlib + bcrypt** — JWT auth & password hashing
- **pypdf + python-docx + python-pptx + openpyxl** — Document parsing
- **pandas + numpy** — Analytics
- **pydantic + pydantic-settings** — Data validation & config
- **pytest + httpx** — Testing

### 4. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your settings (see [Configuration](#configuration) section below).

---

## Configuration

Copy `.env.example` to `.env` and set the required values. Here's a breakdown:

### Required (minimum viable)

```ini
# Server
APP_ENV=development
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Database
SQLITE_PATH=data/mospi_learning.db

# LLM — Choose ONE of Groq or Ollama
GROQ_API_KEY=your_groq_api_key_here
# OR
OLLAMA_BASE_URL=http://localhost:11434
```

### JWT (change in production!)

```ini
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRY_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRY_DAYS=7
```

### iGOT / NSSTA (optional — for course recommendations)

```ini
IGOT_API_BASE_URL=https://api.igotindia.gov.in/v1
IGOT_API_KEY=your_igot_api_key_here
NSSTA_BASE_URL=https://tpac.igotindia.gov.in
NSSTA_API_KEY=your_tpac_api_key_here
```

### Rate Limiting & CORS

```ini
RATE_LIMIT_PER_MINUTE=60
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

### Key Settings File

All configuration lives in **`config/settings.py`** using Pydantic Settings — values are loaded from `.env` automatically. To add a new setting:

1. Add the field to the `Settings` class in `config/settings.py`
2. Add the corresponding key to `.env.example`

---

## Running the Server

### Development Mode

```bash
# Start with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will:
1. Initialize the SQLite database (creates all tables + default admin user)
2. Load core services (CompetencyAnalyzer, CourseRecommender, QuizEngine, etc.)
3. Start the ASGI server on port 8000
4. Print service status to console

**Available URLs:**
- **API Docs (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/api/health

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use Docker (see [Docker Deployment](#docker-deployment)).

### Default Admin Account

On first run, the database is seeded with:

| Field | Value |
|---|---|
| **Username** | `admin` |
| **Password** | `admin123` |
| **Email** | `admin@mospi.gov.in` |
| **Role** | `admin` |

> ⚠️ **Change this password immediately in production!**

---

## Database

### Schema

The database (`data/mospi_learning.db`) is auto-created on startup with these tables:

| Table | Purpose |
|---|---|
| `users` | User accounts (id, username, email, password_hash, roles) |
| `user_roles` | Multi-role support (many-to-many) |
| `competency_scores` | Per-learner competency assessments |
| `quizzes` | Generated quiz metadata |
| `quiz_questions` | Individual questions per quiz |
| `quiz_attempts` | Submitted quiz answers & scores |
| `learning_sessions` | Session tracking (activity, duration, timestamps) |
| `learner_progress` | Per-course completion tracking |
| `audit_log` | Action audit trail |
| `file_uploads` | Uploaded file metadata |
| `db_metadata` | Reference metadata (ChromaDB collection names, etc.) |

### Manual Init

```python
from core.database import init_db
init_db()  # Creates tables + default admin
```

### Backup

```bash
cp data/mospi_learning.db data/mospi_learning.db.backup
```

---

## API Endpoints

All endpoints are prefixed with `/api/`. Full interactive docs at **http://localhost:8000/docs**.

### Health & System

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/health` | Health check (status, DB, version) | ❌ No |

### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/auth/register` | Create new user account | ❌ No |
| `POST` | `/api/auth/login` | Login → get access + refresh tokens | ❌ No |
| `POST` | `/api/auth/refresh` | Exchange refresh token for new access token | ❌ No |
| `GET` | `/api/auth/me` | Get current user profile | ✅ Yes |

**Login Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user_id": "a1b2c3d4",
  "roles": ["admin"]
}
```

### Competency Analysis

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/analyze-profile` | Analyze profile → identify skill gaps | ❌ No |

**Request:**
```json
{
  "designation": "Statistical Officer",
  "profile_text": "5 years of NSSO field survey experience..."
}
```

**Response:**
```json
{
  "current_skills": [{"id": "STAT-001", "name": "Survey Design", "level": "intermediate"}],
  "skill_gaps": [{"id": "TECH-001", "name": "Python for Data Analysis", "priority": "high"}],
  "competency_summary": {"statistical": "intermediate", "technical": "beginner", ...},
  "analysis_summary": "..."
}
```

### Learning Pipeline

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/pipeline/generate-plan` | Full learning plan (batch) | ✅ learner+ |
| `POST` | `/api/pipeline/stream` | Learning plan via SSE streaming | ✅ learner+ |

**Pipeline flow:** Profile Analysis → Gap Identification → Course Matching → Pathway Generation

### Quiz Engine

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/quiz/generate` | Generate MCQs from text |
| `POST` | `/api/quiz/from-file` | Generate MCQs from uploaded file |
| `GET` | `/api/quiz/{quiz_id}` | Get quiz details |
| `POST` | `/api/quiz/attempt` | Submit quiz answers |

### Learning & Analytics

| Method | Endpoint | Description |
|---|---|---|
| Various | `/api/learning/*` | Track sessions, progress |
| Various | `/api/analytics/*` | Learner analytics |
| Various | `/api/admin/*` | Admin overview, workforce data |

### Virtual Assistant

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/assistant` | Chat with AI assistant |

---

## Core Services

Each service is initialized at startup and injected via `app.state`:

### CompetencyAnalyzer (`core/classifier.py`)
Analyzes official profiles against the MoSPI Competency Framework (4 domains: Statistical, Technical, Digital Governance, Behavioural). Uses LLM to score competencies and identify gaps.

### CourseRecommender (`core/rag.py`)
Retrieves relevant iGOT/NSSTA courses for identified skill gaps using semantic search (ChromaDB + embeddings) and LLM-based pathway generation.

### QuizEngine (`core/quiz_engine.py`)
Generates MCQs from learning materials via LLM. Saves to DB. Supports file uploads (PDF, DOCX, PPTX, XLSX) and scoring.

### AttemptTracker (`core/attempt_tracker.py`)
Records quiz attempts with answers, scores, and time tracking.

### FileProcessor (`core/file_processor.py`)
Extracts text from PDF, DOCX, PPTX, and XLSX files.

### LearningTracker (`core/learning_tracker.py`)
Tracks learning sessions, course progress, and hours.

### LearningAnalytics (`core/analytics.py`)
Aggregates workforce competency data, training effectiveness, and predictive gap analysis.

### VirtualAssistant (`core/virtual_assistant.py`)
AI chatbot with intent detection, suggested actions, and resource recommendations.

### Embeddings (`core/embeddings.py`)
Manages the embedding model (Groq or Ollama) and ChromaDB connection.

### Security (`core/security.py`)
Rate limiter with sliding window (configurable requests/minute).

---

## Authentication & Authorization

### Flow

```
Register → Login → Get Tokens → Use Bearer Token
                        ↓
                 Refresh Token (when expired)
```

### JWT Token Structure

```json
{
  "sub": "user_id",
  "roles": ["admin"],
  "exp": <timestamp>
}
```

### Roles & Permissions

| Role | Permissions |
|---|---|
| **admin** | read, write, delete, manage_users, view_analytics |
| **trainer** | read, write, view_analytics |
| **learner** | read, write_own |
| **viewer** | read |

### Middleware Pipeline

```
Request → CORS → Rate Limit → Auth → RBAC → Audit Log → Handler
```

- **CORS:** Configurable origins
- **Rate Limit:** Sliding window (default 60 req/min)
- **Auth:** Validates Bearer token, attaches user_id + roles to request
- **RBAC:** Checks role-based permissions for admin paths
- **Audit Log:** Logs method, path, status code, duration, user

---

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Tests

```bash
pytest tests/test_auth.py -v
pytest tests/test_quiz_engine.py -v
pytest tests/test_competency_framework.py -v
```

### With Coverage

```bash
pip install pytest-cov
pytest tests/ -v --cov=core --cov=api --cov-report=term-missing
```

### Test Files

| File | Tests |
|---|---|
| `test_auth.py` | Login, register, JWT, RBAC |
| `test_database.py` | Schema creation, init |
| `test_quiz_engine.py` | MCQ generation, scoring |
| `test_competency_framework.py` | Competency definitions |
| `test_file_processor.py` | PDF/DOCX/PPTX parsing |
| `test_learning_tracker.py` | Session tracking |
| `test_attempt_tracker.py` | Attempt recording |
| `test_analytics.py` | Analytics aggregation |
| `test_middleware.py` | Auth, RBAC, rate-limit |
| `test_api_routes.py` | End-to-end route tests |

---

## Docker Deployment

### Build & Run

```bash
# Build the image
docker build -t mospi-learning-platform .

# Run
docker run -d \
  --name mospi-backend \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  mospi-learning-platform
```

### Docker Compose (full stack)

```bash
docker compose up --build -d
```

This starts:
- **api** (port 8000) — Backend API
- **frontend** (port 80, 443) — Nginx serving the React frontend

Data is persisted in the `./data` volume.

---

## Troubleshooting

### LLM Not Responding

1. **Groq:** Verify `GROQ_API_KEY` in `.env`
2. **Ollama:** Ensure Ollama is running:
   ```bash
   ollama list          # Check models installed
   ollama serve         # Start if not running
   curl http://localhost:11434/api/tags
   ```

### Database Issues

```bash
# Reset database (WARNING: deletes all data)
rm data/mospi_learning.db
python main.py   # Re-init on startup

# Check DB contents
sqlite3 data/mospi_learning.db ".tables"
sqlite3 data/mospi_learning.db "SELECT * FROM users;"
```

### Port Already in Use

```bash
lsof -i :8000
kill -9 <PID>
```

### ChromaDB Issues

```bash
# Reset vector store
rm -rf data/chroma/*

# Check embeddings model loads
python -c "from core.embeddings import get_embedding_model; get_embedding_model()"
```

### "No authentication token" Error

Make sure to include the header:
```
Authorization: Bearer eyJ...
```

---

## Quick Start Summary

```bash
# 1. Setup
cd /home/devesh/Projects/SIH26
cp .env.example .env
# Edit .env with your API keys

# 2. Activate venv & install
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Run
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Visit
# http://localhost:8000/docs      → API docs
# http://localhost:8000/api/health → Health check

# 5. Login (default admin)
# Username: admin
# Password: admin123
```
