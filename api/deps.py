"""
MoSPI AI Learning Platform — FastAPI Dependency Injection Helpers
Each function retrieves a pre-loaded resource from app.state (set by lifespan).
"""
from fastapi import Request

from core.classifier import CompetencyAnalyzer
from core.rag import CourseRecommender, QuizGenerator
from core.agent import ProfileAgent, PathwayAgent, AssessmentAgent, LMSLayer
from core.judge import SubjectiveAssessor


def get_analyzer(request: Request) -> CompetencyAnalyzer:
    """Get the shared CompetencyAnalyzer instance."""
    return request.app.state.analyzer


def get_recommender(request: Request) -> CourseRecommender:
    """Get the shared CourseRecommender instance."""
    return request.app.state.recommender


def get_quiz_generator(request: Request) -> QuizGenerator:
    """Get the shared QuizGenerator instance."""
    return request.app.state.quiz_generator


def get_lms_layer(request: Request) -> LMSLayer:
    """Get the shared LMSLayer instance."""
    return request.app.state.lms_layer


def get_subjective_assessor(request: Request) -> SubjectiveAssessor:
    """Get the shared SubjectiveAssessor instance."""
    return request.app.state.subjective_assessor
