"""
MoSPI AI Learning Platform — v4.0 API
FastAPI backend wrapping the core capacity building modules.

Run:
    uvicorn main:app --host 0.0.0.0 --port 8001 --reload

Swagger UI:
    http://localhost:8001/docs
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from core.classifier import CompetencyAnalyzer
from core.rag import CourseRecommender, QuizGenerator
from core.agent import ProfileAgent, PathwayAgent, AssessmentAgent, LMSLayer
from core.judge import SubjectiveAssessor

from api.routes import health, classify, retrieve, pipeline, assessment


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load all ML models and resources at startup, clean up at shutdown."""
    print("⚡ MoSPI AI Learning API — Loading intelligence modules...")

    app.state.analyzer = CompetencyAnalyzer()
    print("  ✓ Competency Analyzer loaded")
    app.state.recommender = CourseRecommender()
    print("  ✓ Course Recommender loaded")
    app.state.quiz_generator = QuizGenerator()
    print("  ✓ Quiz Generator loaded")
    app.state.lms_layer = LMSLayer()
    print("  ✓ LMS Orchestration Layer loaded")
    app.state.subjective_assessor = SubjectiveAssessor()
    print("  ✓ Subjective Assessor loaded")

    print("⚡ All modules loaded. MoSPI AI Learning API ready.")
    yield

    print("⚡ Shutting down MoSPI AI Learning API...")


app = FastAPI(
    title="MoSPI AI Learning Platform API",
    description=(
        "RESTful API wrapping official competency analysis, iGOT course recommendations, "
        "MCQ quiz generation, and subjective answer evaluations. "
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
app.include_router(assessment.router)
app.include_router(pipeline.router)


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
        "message": "MoSPI AI Learning API v4.0 — Visit /docs for Swagger UI",
        "docs": "/docs",
        "health": "/api/health",
    }
