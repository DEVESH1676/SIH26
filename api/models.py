"""
Pydantic models for the MoSPI Learning Platform API.
Replaces all IT-ticket-centric models.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── User Models ──────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., max_length=200)
    password: str = Field(..., min_length=8)
    designation: str = Field(..., max_length=200)
    department: str = Field(..., max_length=200)
    role: str = Field(default="learner")


class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    designation: str
    department: str
    roles: list[str]


# ── Course Models ────────────────────────────────────────────

class CourseResponse(BaseModel):
    id: str
    title: str
    description: str
    domain: str
    duration_hours: float
    difficulty: str
    skills: list[str]
    tags: list[str]
    source: str  # "igot" | "local" | "tpac"


class CourseRecommendation(BaseModel):
    courses: list[CourseResponse]
    tpac_programmes: Optional[list[dict]] = []
    estimated_hours: float
    recommended_sequence: list[dict]
    source: str  # "igot" | "fallback"


# ── Competency Models ────────────────────────────────────────

class CompetencyLevel(BaseModel):
    competency_id: str
    competency_name: str
    score: float
    max_score: float = 5.0
    assessed_at: Optional[str] = None
    trend: Optional[str] = None  # "improving" | "stable" | "declining"


class CompetencySummary(BaseModel):
    domain: str
    level: str
    score: float
    strengths: list[str] = []
    gaps: list[str] = []


class CompetencyAnalysis(BaseModel):
    user_id: str
    overall_level: str
    competency_summary: dict[str, CompetencySummary]
    skill_gaps: list[str]
    recommended_pathway: str
    recommended_courses: list[str]
    generated_at: str


# ── Quiz Models ──────────────────────────────────────────────

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: list[str]
    correct_answer: int
    explanation: str
    difficulty: str  # "beginner" | "intermediate" | "advanced"
    category: str


class QuizCreate(BaseModel):
    source_text: str
    num_questions: int = Field(default=10, ge=1, le=50)
    difficulty: str = Field(default="intermediate")
    domain: Optional[str] = None
    source_file: Optional[str] = None


class QuizResponse(BaseModel):
    quiz_id: str
    quiz_title: str
    questions: list[QuizQuestion]
    source: str  # "llm" | "adaptive"


class QuizAttemptRequest(BaseModel):
    quiz_id: str
    answers: dict  # {question_id: selected_option_index}
    time_taken_seconds: int


class QuizResult(BaseModel):
    score: int
    total: int
    percentage: float
    passed: bool
    results: list[dict]


# ── Learning Progress Models ─────────────────────────────────

class LearningSession(BaseModel):
    session_id: str
    activity_type: str
    resource_id: str
    resource_type: str
    duration_seconds: int
    started_at: str
    completed_at: str


class LearningHoursResponse(BaseModel):
    total_sessions: int
    total_hours: float
    average_session_minutes: float
    first_session: Optional[str] = None
    last_session: Optional[str] = None


class CourseProgress(BaseModel):
    course_id: str
    progress: float  # 0-100
    completed_at: Optional[str] = None


# ── Analytics Models ─────────────────────────────────────────

class AdminOverview(BaseModel):
    total_learners: int
    total_learning_sessions: int
    total_quiz_attempts: int
    total_enrolled_courses: int


class WorkforceCompetency(BaseModel):
    competency_id: str
    competency_name: str
    avg_score: float
    assessed_count: int
    mastery_rate: float


class TrainingEffectiveness(BaseModel):
    title: str
    enrolled: int
    avg_score: float
    pass_rate: float


class PredictiveGap(BaseModel):
    competency_id: str
    current_avg: float
    previous_avg: float
    decline_percent: float
    priority: str  # "high" | "medium"


class AdminAnalyticsResponse(BaseModel):
    overview: AdminOverview
    workforce_competency: list[WorkforceCompetency]
    training_effectiveness: list[TrainingEffectiveness]
    predictive_skill_gaps: list[PredictiveGap]


# ── Virtual Assistant Models ─────────────────────────────────

class AssistantRequest(BaseModel):
    message: str
    language: str = Field(default="en")
    user_context: Optional[dict] = None


class AssistantResponse(BaseModel):
    response: str
    suggested_actions: list[dict]
    related_resources: list[dict]
    intent: str


# ── File Upload Models ───────────────────────────────────────

class FileUploadResponse(BaseModel):
    file_id: str
    file_name: str
    file_type: str
    file_size: int
    text_extracted: str
    chunks: list[dict]


class MCQFromFileRequest(BaseModel):
    file_type: str
    num_questions: int = Field(default=10)
    difficulty: str = Field(default="intermediate")
    domain: Optional[str] = None

# ── Legacy Pipeline & Classifier Models ──────────────────────
class LearnerProfileRequest(BaseModel):
    designation: str
    profile_text: str

class LearnerProfileResponse(BaseModel):
    current_skills: list[dict]
    skill_gaps: list[dict]
    competency_summary: dict
    analysis_summary: str

class PipelineStatusEvent(BaseModel):
    stage: str
    message: str
    progress: float

class HealthResponse(BaseModel):
    status: str
    database: str
    version: str
