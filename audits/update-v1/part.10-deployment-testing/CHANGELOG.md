# Part 10 — Deployment, Testing & Final Integration

## Objective
Set up production deployment infrastructure, CI/CD pipelines, comprehensive testing strategy, and finalize all integration points.

## 10.1 Create `.env.example` (NEW FILE)

```bash
# ── Server ─────────────────────────────────────────────────────
APP_NAME="MoSPI AI Learning Platform"
APP_ENV=development
DEBUG=true
HOST=0.0.0.0
PORT=8000

# ── Database ───────────────────────────────────────────────────
SQLITE_PATH=data/mospi_learning.db

# ── ChromaDB ───────────────────────────────────────────────────
CHROMA_PERSIST_DIR=data/chroma
CHROMA_COLLECTION=mospi_embeddings

# ── LLM Provider ───────────────────────────────────────────────
# Option 1: Groq (cloud)
GROQ_API_KEY=gsk_your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_EMBED_MODEL=all-MiniLM-L6-v2

# Option 2: Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.3
OLLAMA_EMBED_MODEL=nomic-embed-text

# ── JWT Authentication ─────────────────────────────────────────
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRY_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRY_DAYS=7

# ── iGOT Karmayogi Integration ─────────────────────────────────
IGOT_API_BASE_URL=https://api.igotindia.gov.in/v1
IGOT_API_KEY=your_igot_api_key_here
IGOT_CACHE_TTL_SECONDS=10800
IGOT_COURSES_PER_REQUEST=20

# ── NSSTA TPAC ─────────────────────────────────────────────────
NSSTA_BASE_URL=https://tpac.igotindia.gov.in
NSSTA_API_KEY=your_tpac_api_key_here

# ── Rate Limiting ──────────────────────────────────────────────
RATE_LIMIT_PER_MINUTE=60

# ── CORS ───────────────────────────────────────────────────────
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# ── Document Processing ────────────────────────────────────────
MAX_DOCUMENT_CHARS=50000
MAX_UPLOAD_SIZE_MB=100
UPLOAD_DIR=data/uploads

# ── Logging ────────────────────────────────────────────────────
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## 10.2 Create `.gitignore` (NEW FILE)

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
*.egg

# Virtual env
.venv/
venv/
env/

# Environment
.env
.env.local
.env.production

# Data
data/mospi_learning.db
data/uploads/*
data/chroma/*
!data/chroma/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Frontend
frontend-v2/node_modules/
frontend-v2/dist/

# Logs
*.log
logs/

# Uploads
uploads/
```

## 10.3 Create `Dockerfile` (NEW FILE)

```dockerfile
FROM python:3.12-slim AS backend

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p data/uploads data/chroma

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM node:20-alpine AS frontend

WORKDIR /app
COPY frontend-v2/package.json frontend-v2/package-lock.json* ./
RUN npm ci
COPY frontend-v2/ .
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend /app/dist /app/frontend-v2/dist
COPY main.py config.py requirements.txt ./
RUN mkdir -p data/uploads data/chroma

ENV APP_ENV=production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 10.4 Create `docker-compose.yml` (NEW FILE)

```yaml
version: "3.9"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./frontend-v2/dist:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - api
    restart: unless-stopped
```

## 10.5 Create `.github/workflows/ci.yml` (NEW FILE)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v --cov=core --cov=api
      - uses: codecov/codecov-action@v4

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm', cache-dependency-path: frontend-v2/package-lock.json }
      - run: cd frontend-v2 && npm ci
      - run: cd frontend-v2 && npm run build
      - run: cd frontend-v2 && npx vitest run

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install ruff flake8
      - run: ruff check core/ api/
      - run: flake8 core/ api/ --max-line-length=120
```

## 10.6 Create `tests/test_core.py` (NEW FILE)

```python
"""
Backend unit tests for core modules.
"""
import pytest
import asyncio
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.classifier import CompetencyAnalyzer
from core.quiz_engine import QuizEngine
from core.attempt_tracker import AttemptTracker
from core.igot_api import IGOTClient
from core.file_processor import FileProcessor
from config.settings import get_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class TestCompetencyAnalyzer:
    def test_analyze_competency(self):
        analyzer = CompetencyAnalyzer()
        user_profile = {
            "designation": "Statistical Analyst",
            "experience_years": 3,
            "current_skills": ["data_entry"],
            "domain": "statistical",
        }
        result = analyzer.analyze(user_profile)
        assert result["overall_level"] is not None
        assert "skill_gaps" in result
        assert "recommended_courses" in result


class TestQuizEngine:
    def test_init_db(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".db", delete=True) as f:
            engine = QuizEngine(db_path=f.name)
            assert os.path.exists(f.name)

    def test_calculate_score(self):
        engine = QuizEngine()
        answers = {"1": 0, "2": 1, "3": 2}
        questions = [
            {"id": "1", "correct_answer": "0"},
            {"id": "2", "correct_answer": "1"},
            {"id": "3", "correct_answer": "2"},
        ]
        result = engine.calculate_score(answers, questions)
        assert result["score"] == 3
        assert result["percentage"] == 100.0


class TestFileProcessor:
    def test_txt_processing(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello world. This is a test document.")
        processor = FileProcessor()
        text = asyncio.get_event_loop().run_until_complete(
            processor.process_file(str(test_file), "txt")
        )
        assert "Hello world" in text

    def test_unsupported_type(self, tmp_path):
        test_file = tmp_path / "test.xyz"
        test_file.write_text("content")
        processor = FileProcessor()
        with pytest.raises(ValueError):
            asyncio.get_event_loop().run_until_complete(
                processor.process_file(str(test_file), "xyz")
            )


class TestIGOTClient:
    def test_init(self):
        client = IGOTClient()
        assert client.base_url is not None
        assert client._headers is not None


class TestAttemptTracker:
    def test_record_and_retrieve(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".db", delete=True) as f:
            tracker = AttemptTracker(db_path=f.name)
            attempt_id = tracker.record_attempt(
                quiz_id="test-quiz", learner_id="learner-1",
                answers={"1": 0}, score=1, total=1,
                time_taken_seconds=30,
            )
            history = tracker.get_learner_history("learner-1")
            assert len(history) == 1
            assert history[0]["score"] == 1

    def test_performance_aggregation(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".db", delete=True) as f:
            tracker = AttemptTracker(db_path=f.name)
            tracker.record_attempt("q1", "l1", {"1": 0}, 1, 1, 30)
            tracker.record_attempt("q2", "l1", {"1": 0}, 2, 2, 60)
            perf = tracker.get_learner_performance("l1")
            assert perf["total_attempts"] == 2
            assert perf["average_score"] == 85.0  # (100 + 75) / 2
```

## 10.7 Create `tests/conftest.py` (NEW FILE)

```python
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
```

## 10.8 Create `nginx.conf` (NEW FILE)

```nginx
server {
    listen 80;
    server_name localhost;

    # Frontend static files
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check
    location /api/health {
        proxy_pass http://api:8000;
    }
}
```

## 10.9 Update `config.py` → `config/settings.py`

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "MoSPI AI Learning Platform"
    app_env: str = "development"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    sqlite_path: str = "data/mospi_learning.db"
    chroma_persist_dir: str = "data/chroma"
    chroma_collection: str = "mospi_embeddings"
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"
    groq_embed_model: str = "all-MiniLM-L6-v2"
    ollama_base_url: Optional[str] = None
    ollama_model: str = "llama3.3"
    ollama_embed_model: str = "nomic-embed-text"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expiry_minutes: int = 60
    jwt_refresh_token_expiry_days: int = 7
    igot_api_base_url: str = "https://api.igotindia.gov.in/v1"
    igot_api_key: Optional[str] = None
    igot_cache_ttl_seconds: int = 10800
    igot_courses_per_request: int = 20
    nssta_base_url: Optional[str] = None
    nssta_api_key: Optional[str] = None
    rate_limit_per_minute: int = 60
    cors_origins: list[str] = ["http://localhost:5173"]
    max_document_chars: int = 50000
    max_upload_size_mb: int = 100
    upload_dir: str = "data/uploads"
    log_level: str = "INFO"
    log_format: str = "json"
    default_quiz_questions: int = 10

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

def get_settings() -> Settings:
    return Settings()
```

## 10.10 Update `main.py` — Final State

```python
"""
MoSPI AI Skill Intelligence & Learning Platform
FastAPI application with learning, assessment, and analytics.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio, os, sys, logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import get_settings
from core.database import init_db
from core.igot_api import IGOTClient
from core.igot_sync import IGOTSyncService
from core.rag import CompetencyAnalyzer, CourseRecommender
from core.quiz_engine import QuizEngine
from core.attempt_tracker import AttemptTracker
from core.file_processor import FileProcessor
from core.learning_tracker import LearningTracker
from core.analytics import LearningAnalytics
from core.virtual_assistant import VirtualAssistant
from api.middleware import setup_cors, auth_middleware, rbac_middleware, rate_limit_middleware, audit_logging_middleware
from api.routes import auth as auth_routes
from api.routes import classify as classify_routes
from api.routes import assessment as assessment_routes
from api.routes import health as health_routes
from api.routes import pipeline as pipeline_routes
from api.routes import history as history_routes
from api.routes import blueprint as blueprint_routes

settings = get_settings()

# ── Logging Setup ──────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format=settings.log_format,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    await asyncio.to_thread(init_db)
    print("  ✓ Database initialized")

    # Initialize core services
    app.state.igot_client = IGOTClient()
    app.state.igot_sync = IGOTSyncService(app.state.igot_client)
    await app.state.igot_sync.start()

    app.state.competency_analyzer = CompetencyAnalyzer()
    app.state.course_recommender = CourseRecommender(app.state.igot_client)
    app.state.quiz_engine = QuizEngine()
    app.state.attempt_tracker = AttemptTracker()
    app.state.file_processor = FileProcessor()
    app.state.learning_tracker = LearningTracker()
    app.state.analytics = LearningAnalytics()
    app.state.virtual_assistant = VirtualAssistant()

    print("  ✓ All services initialized")
    print(f"  ✓ iGOT integration: {'enabled' if settings.igot_api_key else 'disabled'}")
    print(f"  ✓ LLM provider: {'Ollama' if settings.ollama_base_url else 'Groq'}")
    yield
    await app.state.igot_sync.stop()
    print("  ✓ All services stopped")

app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────
setup_cors(app)
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(auth_middleware)
app.middleware("http")(rbac_middleware)
app.middleware("http")(audit_logging_middleware)

# ── API Routes ─────────────────────────────────────────────────
app.include_router(health_routes.router)
app.include_router(auth_routes.router)
app.include_router(classify_routes.router)
app.include_router(assessment_routes.router)
app.include_router(pipeline_routes.router)
app.include_router(history_routes.router)
app.include_router(blueprint_routes.router)

# ── Frontend ───────────────────────────────────────────────────
if os.path.exists("frontend-v2/dist"):
    app.mount("/", StaticFiles(directory="frontend-v2/dist", html=True), name="static")
```

## 10.11 Verification Checklist

### Deployment
- [ ] `.env.example` created with all required variables
- [ ] `.gitignore` excludes sensitive files and data directories
- [ ] `Dockerfile` builds backend + frontend in one image
- [ ] `docker-compose.yml` sets up API + Nginx
- [ ] `nginx.conf` proxies `/api/*` to backend
- [ ] `requirements.txt` includes all new dependencies

### Testing
- [ ] `tests/conftest.py` sets up test fixtures
- [ ] `tests/test_core.py` tests all core modules
- [ ] All tests pass with `pytest tests/`
- [ ] Coverage > 70% for core modules

### CI/CD
- [ ] `.github/workflows/ci.yml` runs tests + lint + build
- [ ] Linting passes (ruff/flake8)
- [ ] Frontend builds successfully

### Integration
- [ ] `main.py` initializes all services in lifespan
- [ ] All API routes registered and accessible
- [ ] Auth middleware protects non-public routes
- [ ] Frontend served from production dist
- [ ] Environment variables properly loaded

## 10.12 Final Deployment Steps

```bash
# 1. Clone and setup
git clone <repo>
cd SIH26

# 2. Install dependencies
pip install -r requirements.txt
cd frontend-v2 && npm ci && cd ..

# 3. Create environment
cp .env.example .env
# Edit .env with actual API keys

# 4. Initialize database
python -c "from core.database import init_db; init_db()"

# 5. Run development server
uvicorn main:app --reload --port 8000
# Frontend dev: cd frontend-v2 && npm run dev

# 6. Run tests
pytest tests/ -v

# 7. Docker deploy
docker compose up -d --build
```
