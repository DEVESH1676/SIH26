# Part 2 — Configuration, Dependencies & Project Setup

## Objective
Replace the IT-ticket-focused configuration with MoSPI learning platform settings, clean up dependencies, and establish the new project foundation.

## Step-by-Step Changes

### 2.1 Delete `config.py` and Create `config/settings.py`

**Delete**: `/home/devesh/Projects/SIH26/config.py`

**Create**: `/home/devesh/Projects/SIH26/config/settings.py`

Replace entire file content with:

```python
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """MoSPI AI Learning Platform settings — loaded from .env with defaults."""

    # ── LLM Configurations ──────────────────────────────────
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    use_groq: bool = True

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-gpu:latest"

    # ── Embedding Configurations ────────────────────────────
    embedding_model_name: str = "all-MiniLM-L6-v2"
    chroma_db_path: str = "./chroma_db"
    collection_name: str = "courses"          # Changed from "tickets"
    
    # ── iGOT Karmayogi Integration ─────────────────────────
    igot_api_base_url: str = "https://api.igot-karmayogi.gov.in/api/v1"
    igot_api_key: str = ""
    igot_cache_ttl_seconds: int = 3600        # Cache catalog for 1 hour
    igot_courses_per_request: int = 50

    # ── Assessment & Quiz ──────────────────────────────────
    max_document_chars: int = 25000            # Increased from 5000
    max_quiz_questions: int = 20               # Increased from 10
    default_quiz_questions: int = 5
    quiz_difficulty_levels: List[str] = ["beginner", "intermediate", "advanced"]

    # ── File Upload ─────────────────────────────────────────
    max_upload_size_mb: int = 50
    allowed_file_types: List[str] = [
        "pdf", "docx", "pptx", "txt", "mp4", "mp3", "wav"
    ]

    # ── Authentication ──────────────────────────────────────
    jwt_secret_key: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expiry_minutes: int = 60
    jwt_refresh_token_expiry_days: int = 7

    # ── Database ────────────────────────────────────────────
    sqlite_path: str = "./data/learning.db"

    # ── Competency Framework ────────────────────────────────
    confidence_threshold: float = 0.75
    medium_confidence_threshold: float = 0.40
    novelty_similarity_threshold: float = 0.20

    # ── Security ────────────────────────────────────────────
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    rate_limit_per_minute: int = 60
    max_login_attempts: int = 5
    password_min_length: int = 8

    # ── Multi-language ──────────────────────────────────────
    supported_languages: List[str] = [
        "en", "hi", "bn", "te", "ta", "mr", "gu", "ur",
        "pa", "ml", "or", "as", "ks", "ne", "sd"
    ]
    default_language: str = "en"

    # ── Logging ─────────────────────────────────────────────
    log_level: str = "INFO"
    log_format: str = "json"  # or "text"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance. Replaces direct config.* access."""
    return Settings()
```

### 2.2 Rewrite `requirements.txt`

**Delete** current content. **Write**:

```txt
# ── Web Framework ─────────────────────────────────────────
fastapi[standard]>=0.135.0
uvicorn[standard]>=0.30.0
python-multipart>=0.0.9

# ── Database & ORM ────────────────────────────────────────
sqlalchemy>=2.0.0
alembic>=1.13.0
aiosqlite>=0.19.0

# ── Vector Database ───────────────────────────────────────
chromadb>=0.5.0

# ── Embeddings & NLP ──────────────────────────────────────
sentence-transformers>=3.0.0

# ── LLM Clients ───────────────────────────────────────────
requests>=2.31.0

# ── Authentication & Security ─────────────────────────────
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
bcrypt>=4.0.0
python-dotenv>=1.0.0

# ── File Processing ───────────────────────────────────────
pypdf>=4.0.0
python-docx>=1.1.0
python-pptx>=0.6.23
openpyxl>=3.1.0

# ── Data & Analytics ──────────────────────────────────────
pandas>=2.2.0
numpy>=1.26.0

# ── Configuration ─────────────────────────────────────────
pydantic>=2.0.0
pydantic-settings>=2.1.0

# ── Async & Scheduling ────────────────────────────────────
python-dateutil>=2.9.0

# ── Testing ───────────────────────────────────────────────
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
```

**Removed packages** (with reasons):
- `langchain`, `langchain-community`, `langchain-groq` — never used; direct `requests` used instead
- `groq` — direct REST calls to Groq API, not the SDK
- `scikit-learn` — replaced by centroid-based cosine similarity
- `plotly` — unused; frontend uses Recharts

### 2.3 Create `.env.example`

```env
# ── LLM Configuration ─────────────────────────────────────
# Use Groq API (recommended for quality) or Ollama (local)
USE_GROQ=true
GROQ_API_KEY=gsk-xxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile

# Local fallback
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-gpu:latest

# ── iGOT Karmayogi Integration ────────────────────────────
IGOT_API_BASE_URL=https://api.igot-karmayogi.gov.in/api/v1
IGOT_API_KEY=your-igot-api-key-here

# ── Database ──────────────────────────────────────────────
CHROMA_DB_PATH=./chroma_db
COLLECTION_NAME=courses
SQLITE_PATH=./data/learning.db

# ── Authentication ────────────────────────────────────────
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRY_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRY_DAYS=7

# ── Security ──────────────────────────────────────────────
MAX_UPLOAD_SIZE_MB=50
RATE_LIMIT_PER_MINUTE=60
PASSWORD_MIN_LENGTH=8

# ── Logging ───────────────────────────────────────────────
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 2.4 Update `.gitignore`

**Append** these rules:
```
# ── Learning Platform ─────────────────────────────────────
data/learning.db
data/uploads/*
!data/uploads/.gitkeep
chroma_db/.chroma
.env
__pycache__/
*.pyc
.venv/
venv/
*.egg-info/
dist/
build/
frontend-v2/dist/
frontend-v2/node_modules/
```

### 2.5 Update `main.py` Imports

In `main.py`, replace:
```python
import config
```
with:
```python
from config.settings import get_settings
settings = get_settings()
```

And update all `config.` references:
- `config.USE_GROQ` → `settings.use_groq`
- `config.GROQ_API_KEY` → `settings.groq_api_key`
- `config.OLLAMA_BASE_URL` → `settings.ollama_base_url`
- `config.CHROMA_DB_DIR` → `settings.chroma_db_path`
- `config.COLLECTION_NAME` → `settings.collection_name`

### 2.6 Verification Checklist

- [ ] `pip install -r requirements.txt` completes without errors
- [ ] `.env` file created from `.env.example` with actual API keys
- [ ] `from config.settings import get_settings` works
- [ ] All `config.` references replaced with `settings.`
- [ ] Old `config.py` deleted
- [ ] `.env` is in `.gitignore`
- [ ] `venv` recreated: `rm -rf venv && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
