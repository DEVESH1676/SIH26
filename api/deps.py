"""
MoSPI AI Learning Platform — FastAPI Dependency Injection Helpers
Each function retrieves a pre-loaded resource from app.state (set by lifespan).
"""
from fastapi import Request

from core.igot_api import IGOTClient
from core.rag import CompetencyAnalyzer, CourseRecommender
from core.quiz_engine import QuizEngine
from core.attempt_tracker import AttemptTracker
from core.file_processor import FileProcessor
from core.learning_tracker import LearningTracker
from core.analytics import LearningAnalytics
from core.virtual_assistant import VirtualAssistant


def get_analyzer(request: Request) -> CompetencyAnalyzer:
    return request.app.state.competency_analyzer

def get_recommender(request: Request) -> CourseRecommender:
    return request.app.state.course_recommender

def get_quiz_engine(request: Request) -> QuizEngine:
    return request.app.state.quiz_engine

def get_igot_client(request: Request) -> IGOTClient:
    return request.app.state.igot_client

def get_attempt_tracker(request: Request) -> AttemptTracker:
    return request.app.state.attempt_tracker

def get_file_processor(request: Request) -> FileProcessor:
    return request.app.state.file_processor

def get_learning_tracker(request: Request) -> LearningTracker:
    return request.app.state.learning_tracker

def get_analytics(request: Request) -> LearningAnalytics:
    return request.app.state.analytics

def get_virtual_assistant(request: Request) -> VirtualAssistant:
    return request.app.state.virtual_assistant
