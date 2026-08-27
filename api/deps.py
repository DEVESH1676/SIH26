"""
Nexus AI — FastAPI Dependency Injection Helpers
Each function retrieves a pre-loaded resource from app.state (set by lifespan).
"""
from fastapi import Request

from core.classifier import TicketClassifier
from core.rag import ResolutionEngine
from core.agent import TriageAgent, ResolutionAgent, AutomationDiscoveryAgent
from core.judge import ResolutionJudge
from core.feedback import FeedbackStore


def get_classifier(request: Request) -> TicketClassifier:
    """Get the shared TicketClassifier instance."""
    return request.app.state.classifier


def get_rag_engine(request: Request) -> ResolutionEngine:
    """Get the shared ResolutionEngine instance."""
    return request.app.state.rag_engine


def get_triage_agent(request: Request) -> TriageAgent:
    """Get the shared TriageAgent instance."""
    return request.app.state.triage_agent


def get_resolution_agent(request: Request) -> ResolutionAgent:
    """Get the shared ResolutionAgent instance."""
    return request.app.state.resolution_agent


def get_automation_agent(request: Request) -> AutomationDiscoveryAgent:
    """Get the shared AutomationDiscoveryAgent instance."""
    return request.app.state.automation_agent


def get_judge(request: Request) -> ResolutionJudge:
    """Get the shared ResolutionJudge instance."""
    return request.app.state.judge


def get_feedback_store(request: Request) -> FeedbackStore:
    """Get the shared FeedbackStore instance."""
    return request.app.state.feedback_store
