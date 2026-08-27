"""
Nexus AI Ticket Intelligence Platform — v4.0 API
FastAPI backend wrapping the core intelligence modules.

Run:
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Swagger UI:
    http://localhost:8000/docs
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from core.classifier import TicketClassifier
from core.rag import ResolutionEngine
from core.agent import TriageAgent, ResolutionAgent, AutomationDiscoveryAgent
from core.judge import ResolutionJudge
from core.feedback import FeedbackStore

from api.routes import health, classify, retrieve, pipeline, blueprint, history


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load all ML models and resources at startup, clean up at shutdown."""
    print("⚡ Nexus AI API — Loading intelligence modules...")

    # Load heavy resources once (mirrors Streamlit's @st.cache_resource)
    app.state.classifier = TicketClassifier()
    print("  ✓ Classifier loaded")
    app.state.rag_engine = ResolutionEngine()
    print("  ✓ RAG Engine loaded")
    app.state.triage_agent = TriageAgent()
    print("  ✓ Triage Agent loaded")
    app.state.resolution_agent = ResolutionAgent()
    print("  ✓ Resolution Agent loaded")
    app.state.automation_agent = AutomationDiscoveryAgent()
    print("  ✓ Automation Discovery Agent loaded")
    app.state.judge = ResolutionJudge()
    print("  ✓ Resolution Judge loaded")
    app.state.feedback_store = FeedbackStore()
    print("  ✓ Feedback Store loaded")

    print("⚡ All modules loaded. Nexus AI API ready.")
    yield

    # Shutdown
    print("⚡ Shutting down Nexus AI API...")
    if hasattr(app.state, "feedback_store"):
        app.state.feedback_store.close()


app = FastAPI(
    title="Nexus AI — Ticket Intelligence API",
    description=(
        "RESTful API wrapping the Nexus AI classification cascade, "
        "RAG retrieval, agent-based triage, and LLM-as-Judge quality evaluation. "
        "Supports both synchronous requests and Server-Sent Events for real-time streaming."
    ),
    version="4.0.0",
    lifespan=lifespan,
)

# CORS — allow React frontend in dev (Vite default ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # CRA / Next.js default
        "http://localhost:8080",  # Alternative dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(health.router)
app.include_router(classify.router)
app.include_router(retrieve.router)
app.include_router(pipeline.router)
app.include_router(blueprint.router)
app.include_router(history.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response

@app.get("/", include_in_schema=False)
def root():
    """Root redirect — points users to Swagger UI."""
    return {
        "message": "Nexus AI API v4.0 — Visit /docs for Swagger UI",
        "docs": "/docs",
        "health": "/api/health",
    }
