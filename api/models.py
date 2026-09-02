"""
MoSPI AI Learning Platform — Pydantic Data Contracts
Every model mirrors the exact dict keys returned by core LMS modules.
"""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


# ── Profiling Models ──────────────────────────────────────
class LearnerProfileRequest(BaseModel):
    """Input for Competency Analysis."""
    designation: str = Field(..., min_length=2, max_length=200, description="Official's designation (e.g. Statistical Officer)")
    department: Optional[str] = Field(None, description="Department or Cadre (e.g., ISS, SSS)")
    education: Optional[str] = Field(None, description="Educational background")
    training_history: Optional[list[str]] = Field(None, description="Previously completed courses/training")
    profile_text: str = Field(..., min_length=5, max_length=5000, description="Summary of official's experience, background, and current duties")


class LearnerProfileResponse(BaseModel):
    """Output of Competency Analysis."""
    current_skills: dict[str, list[str]]
    skill_gaps: dict[str, list[str]]
    analysis_summary: str


# ── Course Recommendation & Pathway Models ─────────────────
class PathwayRequest(BaseModel):
    """Input for Learning Pathway recommendation."""
    skill_gaps: list[str] = Field(..., description="List of missing skills identified for the official")


class CourseRecommendation(BaseModel):
    """Single iGOT course recommendation."""
    course_id: str
    course_name: str
    domain: str
    skills_covered: str
    description: str


class PathwayResponse(BaseModel):
    """Output of Course Recommender."""
    suggested_pathway: str
    courses: list[dict]


# ── Quiz & Assessment Models ────────────────────────────────
class QuizRequest(BaseModel):
    """Input for MCQ generation."""
    document_text: str = Field(..., min_length=20, max_length=10000, description="Uploaded learning material text")
    num_questions: int = Field(default=5, ge=1, le=10, description="Number of questions to generate")


class MCQQuestion(BaseModel):
    """Single Multiple Choice Question."""
    question_id: int
    question: str
    options: list[str]
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    """Generated Quiz from learning material."""
    quiz_title: str
    questions: list[MCQQuestion]


# ── Subjective Answer Evaluation Models ─────────────────────
class SubjectiveAnswerRequest(BaseModel):
    """Input for evaluating a learner's subjective answer."""
    question: str = Field(..., min_length=5, description="Assessment question asked to learner")
    expected_key_points: str = Field(..., min_length=5, description="Key concepts required in correct answer")
    learner_answer: str = Field(..., min_length=2, description="The answer provided by the official")


class SubjectiveAnswerResponse(BaseModel):
    """Evaluation result for subjective answer."""
    accuracy: int
    comprehension: int
    completeness: int
    overall: float
    passed: bool
    feedback: str


# ── SSE Event Models ───────────────────────────────────────
class PipelineStatusEvent(BaseModel):
    """Streamed during learning plan creation via SSE."""
    stage: str       # profiling | identifying_gaps | matching_courses | building_pathway | complete
    message: str     # Human-readable status message
    progress: float  # 0.0 to 1.0


# ── Health ─────────────────────────────────────────────────
class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    models_loaded: bool
    version: str = "4.0.0"
    domain: str = "MoSPI AI Learning Platform"


# ── Auth & SSO Models ──────────────────────────────────────
class SSOLoginRequest(BaseModel):
    """Input for Jan Parichay Mock SSO."""
    email: str
    password: Optional[str] = None

class AuthResponse(BaseModel):
    """Output for successful authentication."""
    token: str
    user: dict
    status: str
    provider: str


# ── File Upload Models ─────────────────────────────────────
class FileUploadResponse(BaseModel):
    """Response after document parsing."""
    filename: str
    content_length: int
    extracted_text: str
    status: str = "success"


# ── Progress & Tracking Models ─────────────────────────────
class QuizAttemptRequest(BaseModel):
    """Log a quiz attempt."""
    learner_id: str
    quiz_id: str
    score: float
    passed: bool

class QuizAttemptResponse(BaseModel):
    """Response after logging a quiz attempt."""
    status: str = "success"
    message: str


# ── Admin Dashboard Models ─────────────────────────────────
class TopSkillGap(BaseModel):
    skill: str
    count: int

class AdminOverviewResponse(BaseModel):
    status: str = "success"
    data: dict # Could be typed further if needed

class AdminWorkforceResponse(BaseModel):
    status: str = "success"
    data: dict
