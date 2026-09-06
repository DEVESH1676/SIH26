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
from core.classifier import CompetencyAnalyzer
from core.rag import CourseRecommender
from core.quiz_engine import QuizEngine
from core.attempt_tracker import AttemptTracker
from core.file_processor import FileProcessor
from core.learning_tracker import LearningTracker
from core.analytics import LearningAnalytics
from core.virtual_assistant import VirtualAssistant
from api.middleware import setup_cors, auth_middleware, rbac_middleware, rate_limit_middleware, audit_logging_middleware
from api.routes import auth as auth_routes
from api.routes import classify as classify_routes
from api.routes import health as health_routes
from api.routes import pipeline as pipeline_routes
from api.routes import quiz as quiz_routes
from api.routes import courses as courses_routes
from api.routes import analytics as analytics_routes
from api.routes import assistant as assistant_routes

settings = get_settings()

# ── Logging Setup ──────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format=settings.log_format,
)

def _init_app_state(app: FastAPI):
    """Initialize all app state — used by both lifespan and fallback."""
    # Initialize database
    init_db()

    # Core services — store with canonical names
    app.state.competency_analyzer = CompetencyAnalyzer()
    app.state.course_recommender = CourseRecommender()
    # Aliases for route compatibility (pipeline.py references these)
    app.state.analyzer = app.state.competency_analyzer
    app.state.recommender = app.state.course_recommender
    app.state.quiz_engine = QuizEngine()
    app.state.attempt_tracker = AttemptTracker()
    app.state.file_processor = FileProcessor()
    app.state.learning_tracker = LearningTracker()
    app.state.analytics = LearningAnalytics()
    app.state.virtual_assistant = VirtualAssistant()

    print("  ✓ All services initialized")
    print(f"  ✓ iGOT integration: {'enabled' if settings.igot_api_key else 'disabled'}")
    print(f"  ✓ LLM provider: {'Ollama' if settings.ollama_base_url else 'Groq'}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not hasattr(app.state, "competency_analyzer"):
        _init_app_state(app)
    yield
    print("  ✓ All services stopped")

app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    lifespan=lifespan,
)

# ── Fallback: Initialize state at module load ──────────────────
# This ensures state is available even when lifespan isn't triggered
# (e.g., TestClient, direct import, or dev mode without uvicorn)
if not hasattr(app.state, "competency_analyzer"):
    _init_app_state(app)

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
app.include_router(pipeline_routes.router)
app.include_router(quiz_routes.router)
app.include_router(courses_routes.router)
app.include_router(analytics_routes.router)
app.include_router(assistant_routes.router)

# ── Frontend ───────────────────────────────────────────────────
# Serve frontend-v2 static build
if os.path.exists("frontend-v2/dist"):
    app.mount("/", StaticFiles(directory="frontend-v2/dist", html=True), name="static")
elif os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
print(f"  ✓ Frontend: {'frontend-v2/dist' if os.path.exists('frontend-v2/dist') else 'frontend/dist' if os.path.exists('frontend/dist') else 'not found (API-only mode)'}")
