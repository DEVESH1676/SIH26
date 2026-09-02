# Part 1 — New Files Required

## 1.1 Domain Definition Files

### `core/competency_framework.py` (NEW)
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

### `data/competency_framework.json` (NEW)
Complete JSON file with all competency definitions, mapping to NSSTA job roles, iGOT course IDs, and assessment criteria.

### `data/job_role_matrix.csv` (NEW)
Maps designations/roles in MoSPI/NSSTA to required competencies:
```
designation,department,statistical_comp,technical_comp,digital_gov,behavioural_comp,experience_level
Statistical Officer,CSO,STAT-001;STAT-002;STAT-003,TECH-001;TECH-003,DG-001,BEH-002;BEH-003,intermediate
Data Entry Operator,NSSTA,STAT-001,TECH-001;TECH-003,DG-001,BEH-002,beginner
```

## 1.2 Authentication & Security

### `core/auth.py` (NEW)
JWT-based authentication with:
- User login/logout
- Password hashing (bcrypt)
- Token refresh
- RBAC middleware decorators
- SSO integration hook (OIDC/SAML)

### `core/security.py` (NEW)
- Input sanitization for prompt injection prevention
- Rate limiting decorator
- Audit log writer
- Data encryption utilities (for PII at rest)

### `api/routes/auth.py` (NEW)
Endpoints:
- `POST /api/auth/register` — Admin-only user registration
- `POST /api/auth/login` — SSO + password login
- `POST /api/auth/refresh` — Refresh JWT token
- `POST /api/auth/logout` — Invalidate token
- `GET /api/auth/me` — Get current user profile

### `api/middleware.py` (NEW)
- Authentication middleware (JWT validation)
- RBAC middleware (role-based access)
- Rate limiting middleware
- Request logging middleware
- CORS refined middleware (production settings)

## 1.3 iGOT Integration

### `core/igot_api.py` (NEW)
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

### `core/igot_sync.py` (NEW)
Background task for syncing iGOT catalog:
- Periodic sync (cron/asyncio)
- Incremental updates
- Fallback to cached catalog
- Error handling and retry logic

## 1.4 File Processing

### `core/file_processor.py` (NEW)
Handles multi-format document processing:
```python
class FileProcessor:
    async def process_pdf(self, file) -> str  # Extract text
    async def process_docx(self, file) -> str
    async def process_pptx(self, file) -> str
    async def process_video(self, file) -> tuple[str, list[dict]]  # text + chapter marks
    async def process_speech(self, file) -> str  # Audio transcription
```

### `data/uploads/` (NEW DIRECTORY)
Secure upload directory with:
- File type validation
- Size limits
- Temporary file cleanup
- Access control

## 1.5 Dashboard Data

### `core/analytics.py` (NEW)
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

### `api/routes/analytics.py` (NEW)
Endpoints:
- `GET /api/analytics/learner/profile` — Learner dashboard data
- `GET /api/analytics/learner/progress` — Progress tracking
- `GET /api/analytics/learner/history` — Learning history
- `GET /api/analytics/admin/overview` — Admin overview
- `GET /api/analytics/admin/workforce` — Workforce analytics
- `GET /api/analytics/admin/predictions` — Predictive analytics

## 1.6 Quiz & Assessment Engine

### `core/quiz_engine.py` (NEW)
```python
class QuizEngine:
    async def generate_mcqs(self, document: str, difficulty: str, num_questions: int) -> dict
    async def generate_subjective(self, document: str, num_questions: int) -> dict
    async def adaptive_quiz(self, learner_id: str, topic: str) -> dict  # Difficulty adapts to performance
    async def quiz_review(self, quiz_id: str, learner_id: str) -> dict
    async def save_quiz(self, quiz_data: dict) -> str  # Returns quiz_id
    async def get_quiz(self, quiz_id: str) -> dict
```

### `core/attempt_tracker.py` (NEW)
Tracks quiz attempts over time:
```python
class AttemptTracker:
    async def record_attempt(self, quiz_id: str, learner_id: str, answers: dict) -> dict
    async def get_attempt_history(self, quiz_id: str, learner_id: str) -> list[dict]
    async def get_learner_performance(self, learner_id: str, time_range: str) -> dict
```

## 1.7 Virtual Assistant

### `core/virtual_assistant.py` (NEW)
AI-powered learning assistant:
```python
class VirtualAssistant:
    async def respond(self, user_message: str, user_context: dict) -> dict
    # Returns: response_text, suggested_actions, related_resources
```

## 1.8 Configuration

### `.env.example` (NEW)
Template with all required environment variables.

### `config/settings.py` (NEW)
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

## 1.9 Database Migrations

### `db/migrations/` (NEW)
Alembic migration files for new schema:
- `001_initial_learning_schema.py`
- `002_user_auth_schema.py`
- `003_quiz_attempt_schema.py`
- `004_learning_hours_schema.py`

### `db/models.py` (NEW)
SQLAlchemy models for the new schema (users, courses, assessments, progress, etc.)

## 1.10 Deployment & Ops

### `Dockerfile` (NEW)
Multi-stage Docker build for backend and frontend.

### `docker-compose.yml` (NEW)
Docker Compose for local dev (FastAPI + React + ChromaDB + PostgreSQL).

### `.github/workflows/ci.yml` (NEW)
GitHub Actions CI pipeline: lint → test → build → security scan.

### `scripts/init_competency_framework.py` (NEW)
Script to populate initial competency framework data.

### `scripts/sync_igot_catalog.py` (NEW)
Script to sync iGOT course catalog.

### `scripts/generate_mock_data.py` (NEW)
Generate realistic MoSPI learner data for testing.

## 1.11 Documentation

### `docs/api-reference.md` (NEW)
Complete API reference for all endpoints.

### `docs/deployment.md` (NEW)
Deployment guide for government cloud.

### `docs/security.md` (NEW)
Security architecture and compliance documentation.

### `docs/contributing.md` (NEW)
Developer contribution guide.
