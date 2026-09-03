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
from api.routes import health as health_routes
from api.routes import pipeline as pipeline_routes

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
app.include_router(pipeline_routes.router)

# ── Frontend ───────────────────────────────────────────────────
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
