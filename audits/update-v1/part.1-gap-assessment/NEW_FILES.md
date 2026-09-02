# Part 1 — New Files Required

## 1.1 Domain Definition Files

### `core/competency_framework.py` (NEW) [CONSOLIDATED]
```python
"""
MoSPI Competency Framework — Domain-specific competency definitions
for India's Official Statistical System.
"""

STATISTICAL_COMPETENCIES = {
    "survey_design": {
        "id": "STAT-001",
        "name": "Survey Design & Methodology",
        "levels": {
            "beginner": ["Basic survey principles", "Questionnaire formatting"],
            "intermediate": ["Sampling frame development", "Pilot testing design"],
            "advanced": ["Complex multi-stage sampling", "Mixed-methods design"]
        }
    },
    "sampling": {
        "id": "STAT-002",
        "name": "Sampling Techniques",
        "levels": {
            "beginner": ["Simple random sampling", "Stratified sampling"],
            "intermediate": ["Cluster sampling", "Systematic sampling"],
            "advanced": ["Multistage sampling", "Probability proportional to size"]
        }
    },
    # ... all domains from problem statement
}

TECHNICAL_COMPETENCIES = {
    "python": {"id": "TECH-001", "name": "Python for Data Analysis"},
    "r": {"id": "TECH-002", "name": "R Programming"},
    "sql": {"id": "TECH-003", "name": "SQL & Database Management"},
    "gis": {"id": "TECH-004", "name": "GIS & Spatial Analysis"},
    # ... all technical skills
}

DIGITAL_GOVERNANCE = {
    "cybersecurity": {"id": "DG-001", "name": "Cybersecurity Fundamentals"},
    "data_privacy": {"id": "DG-002", "name": "Data Privacy & Protection"},
    "digital_signatures": {"id": "DG-003", "name": "Digital Signatures & Certification"},
}

BEHAVIOURAL_COMPETENCIES = {
    "leadership": {"id": "BEH-001", "name": "Leadership & Team Management"},
    "communication": {"id": "BEH-002", "name": "Effective Communication"},
    "ethics": {"id": "BEH-003", "name": "Ethics & Integrity"},
}
```

**Status**: Consolidated into `data/mospi_frac.json` and dynamically handled by `core/classifier.py` for the MVP.

### `data/competency_framework.json` (NEW) [DONE]
Complete JSON file with all competency definitions, mapping to NSSTA job roles, iGOT course IDs, and assessment criteria.

**Status**: Implemented as `data/mospi_frac.json` containing FRAC domain definitions and criteria.

### `data/job_role_matrix.csv` (NEW) [OUT OF SCOPE]
Maps designations/roles in MoSPI/NSSTA to required competencies:
```
designation,department,statistical_comp,technical_comp,digital_gov,behavioural_comp,experience_level
Statistical Officer,CSO,STAT-001;STAT-002;STAT-003,TECH-001;TECH-003,DG-001,BEH-002;BEH-003,intermediate
Data Entry Operator,NSSTA,STAT-001,TECH-001;TECH-003,DG-001,BEH-002,beginner
```

**Status**: Hardcoded matrix skipped for MVP. Job roles are evaluated dynamically by the LLM reasoning engines based on FRAC definitions.

## 1.2 Authentication & Security

### `core/auth.py` (NEW) [DONE]
JWT-based authentication with:
- User login/logout
- Password hashing (bcrypt)
- Token refresh
- RBAC middleware decorators
- SSO integration hook (OIDC/SAML)

**Status**: JWT-based authentication implemented as a lightweight mock for the MVP with `@require_role` decorators to secure admin routes. Full SSO/bcrypt deferred.

### `core/security.py` (NEW) [OUT OF SCOPE]
- Input sanitization for prompt injection prevention
- Rate limiting decorator
- Audit log writer
- Data encryption utilities (for PII at rest)

**Status**: Out of scope for hackathon MVP. Input sanitization is naturally handled by Pydantic; rate limiting and encryption deferred.

### `api/routes/auth.py` (NEW) [OUT OF SCOPE]
Endpoints:
- `POST /api/auth/register` — Admin-only user registration
- `POST /api/auth/login` — SSO + password login
- `POST /api/auth/refresh` — Refresh JWT token
- `POST /api/auth/logout` — Invalidate token
- `GET /api/auth/me` — Get current user profile

**Status**: Full auth routes deferred for hackathon MVP. Admin roles and user context are mocked at the decorator level.

### `api/middleware.py` (NEW) [CONSOLIDATED]
- Authentication middleware (JWT validation)
- RBAC middleware (role-based access)
- Rate limiting middleware
- Request logging middleware
- CORS refined middleware (production settings)

**Status**: Consolidated into `main.py` (CORS, basic logging) and `core/auth.py` (RBAC). Rate limiting and JWT validation deferred for MVP.

## 1.3 iGOT Integration

### `core/igot_api.py` (NEW) [OUT OF SCOPE]
Full iGOT Karmayogi API adapter:
```python
class IGOTClient:
    async def get_course_catalog(self) -> list[dict]
    async def get_course_details(self, course_id: str) -> dict
    async def enroll_user(self, user_id: str, course_id: str) -> dict
    async def get_user_enrollments(self, user_id: str) -> list[dict]
    async def get_course_completion(self, user_id: str, course_id: str) -> dict
    async def search_courses(self, keywords: str, domain: str = None) -> list[dict]
```

**Status**: True API integration is out of scope for the MVP due to access limitations. Implemented statically via `CourseRecommender` and `mock_igot_catalog.csv` ingested into ChromaDB.

### `core/igot_sync.py` (NEW) [OUT OF SCOPE]
Background task for syncing iGOT catalog:
- Periodic sync (cron/asyncio)
- Incremental updates
- Fallback to cached catalog
- Error handling and retry logic

**Status**: Syncing logic deferred. The catalog is pre-loaded statically into ChromaDB for the MVP.

## 1.4 File Processing

### `core/file_processor.py` (NEW) [DONE]
Handles multi-format document processing:
```python
class FileProcessor:
    async def process_pdf(self, file) -> str  # Extract text
    async def process_docx(self, file) -> str
    async def process_pptx(self, file) -> str
    async def process_video(self, file) -> tuple[str, list[dict]]  # text + chapter marks
    async def process_speech(self, file) -> str  # Audio transcription
```

**Status**: Implemented as `core/parser.py` which robustly mocks PyPDF, python-docx, and whisper extraction for MVP performance.

### `data/uploads/` (NEW DIRECTORY) [OUT OF SCOPE]
Secure upload directory with:
- File type validation
- Size limits
- Temporary file cleanup
- Access control

**Status**: Persistent storage of uploads is deferred. The system currently handles file parsing purely in-memory or via stubbed mock paths.

## 1.5 Dashboard Data

### `core/analytics.py` (NEW) [CONSOLIDATED]
Learning analytics engine:
```python
class LearningAnalytics:
    def get_learner_dashboard(self, learner_id: str) -> dict
    def get_admin_dashboard(self, org_id: str) -> dict
    def get_course_effectiveness(self, course_id: str) -> dict
    def get_workforce_competency_distribution(self, org_id: str) -> dict
    def get_predictive_skill_needs(self, org_id: str) -> dict
    def get_training_roi(self, org_id: str, period: str) -> dict
```

**Status**: Consolidated into `api/routes/admin.py`.

### `api/routes/analytics.py` (NEW) [CONSOLIDATED]
Endpoints:
- `GET /api/analytics/learner/profile` — Learner dashboard data
- `GET /api/analytics/learner/progress` — Progress tracking
- `GET /api/analytics/learner/history` — Learning history
- `GET /api/analytics/admin/overview` — Admin overview
- `GET /api/analytics/admin/workforce` — Workforce analytics
- `GET /api/analytics/admin/predictions` — Predictive analytics

**Status**: Consolidated into `api/routes/admin.py` which provides mocked JSON responses for Admin Dashboard data to satisfy MVP requirements.

## 1.6 Quiz & Assessment Engine

### `core/quiz_engine.py` (NEW) [CONSOLIDATED]
```python
class QuizEngine:
    async def generate_mcqs(self, document: str, difficulty: str, num_questions: int) -> dict
    async def generate_subjective(self, document: str, num_questions: int) -> dict
    async def adaptive_quiz(self, learner_id: str, topic: str) -> dict  # Difficulty adapts to performance
    async def quiz_review(self, quiz_id: str, learner_id: str) -> dict
    async def save_quiz(self, quiz_data: dict) -> str  # Returns quiz_id
    async def get_quiz(self, quiz_id: str) -> dict
```

**Status**: Consolidated into `core/rag.py` as `QuizGenerator` for simpler LLM generation flow without needing a separate engine file.

### `core/attempt_tracker.py` (NEW) [OUT OF SCOPE]
Tracks quiz attempts over time:
```python
class AttemptTracker:
    async def record_attempt(self, quiz_id: str, learner_id: str, answers: dict) -> dict
    async def get_attempt_history(self, quiz_id: str, learner_id: str) -> list[dict]
    async def get_learner_performance(self, learner_id: str, time_range: str) -> dict
```

**Status**: Attempt tracking over time is deferred for the MVP. Current architecture handles single-attempt evaluation directly via `AssessmentAgent`.

## 1.7 Virtual Assistant

### `core/virtual_assistant.py` (NEW) [CONSOLIDATED]
AI-powered learning assistant:
```python
class VirtualAssistant:
    async def respond(self, user_message: str, user_context: dict) -> dict
    # Returns: response_text, suggested_actions, related_resources
```

**Status**: Consolidated into the `LMSLayer` and individual agents (`ProfileAgent`, `PathwayAgent`, `AssessmentAgent`) inside `core/agent.py`.

## 1.8 Configuration

### `.env.example` (NEW) [DONE]
Template with all required environment variables.

**Status**: Created successfully.

### `config/settings.py` (NEW) [CONSOLIDATED]
Pydantic-based settings management (replaces global config.py):
```python
class Settings(BaseSettings):
    # LLM
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-gpu:latest"
    
    # iGOT
    igot_api_base: str = "https://api.igot-karmayogi.gov.in"
    igot_api_key: str = ""
    igot_refresh_interval: int = 3600
    
    # Auth
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 60
    
    # Security
    max_upload_size_mb: int = 50
    allowed_file_types: list[str] = ["pdf", "docx", "pptx", "mp4", "mp3"]
    
    # Database
    sqlite_path: str = "data/learning.db"
    chroma_db_path: str = "chroma_db"
    
    class Config:
        env_file = ".env"
```

**Status**: Implemented simply as `config.py` using `dotenv` for the MVP instead of heavy Pydantic models.

## 1.9 Database Migrations

### `db/migrations/` (NEW) [OUT OF SCOPE]
Alembic migration files for new schema:
- `001_initial_learning_schema.py`
- `002_user_auth_schema.py`
- `003_quiz_attempt_schema.py`
- `004_learning_hours_schema.py`

**Status**: Alembic migrations and PostgreSQL deferred. The system uses a simple local SQLite file (`learner_progress.db`) for MVP portability.

### `db/models.py` (NEW) [OUT OF SCOPE]
SQLAlchemy models for the new schema (users, courses, assessments, progress, etc.)

**Status**: SQLAlchemy deferred in favor of direct local storage for the MVP.

## 1.10 Deployment & Ops

### `Dockerfile` (NEW) [OUT OF SCOPE]
Multi-stage Docker build for backend and frontend.

**Status**: Out of scope for hackathon MVP. Local execution is the target.

### `docker-compose.yml` (NEW) [OUT OF SCOPE]
Docker Compose for local dev (FastAPI + React + ChromaDB + PostgreSQL).

**Status**: Out of scope for hackathon MVP.

### `.github/workflows/ci.yml` (NEW) [OUT OF SCOPE]
GitHub Actions CI pipeline: lint → test → build → security scan.

**Status**: Out of scope for hackathon MVP.

### `scripts/init_competency_framework.py` (NEW) [OUT OF SCOPE]
Script to populate initial competency framework data.

**Status**: Competency framework is dynamically sourced directly from `data/mospi_frac.json`.

### `scripts/sync_igot_catalog.py` (NEW) [OUT OF SCOPE]
Script to sync iGOT course catalog.

**Status**: Handled via mock dataset.

### `scripts/generate_mock_data.py` (NEW) [OUT OF SCOPE]
Generate realistic MoSPI learner data for testing.

**Status**: Not required; evaluation pipelines simulate learner data on the fly.

## 1.11 Documentation

### `docs/api-reference.md` (NEW) [OUT OF SCOPE]
Complete API reference for all endpoints.

**Status**: Out of scope.

### `docs/deployment.md` (NEW) [OUT OF SCOPE]
Deployment guide for government cloud.

**Status**: Out of scope.

### `docs/security.md` (NEW) [OUT OF SCOPE]
Security architecture and compliance documentation.

**Status**: Out of scope.

### `docs/contributing.md` (NEW) [OUT OF SCOPE]
Developer contribution guide.

**Status**: Out of scope.
