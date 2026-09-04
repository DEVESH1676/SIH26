"""
MoSPI AI Learning Platform — Health Check Endpoint
GET /api/health — Returns API status and loaded LMS model information.
"""
from fastapi import APIRouter, Request

from api.models import HealthResponse

router = APIRouter(prefix="/api", tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health_check(request: Request) -> HealthResponse:
    """Returns API health status and loaded model information."""
    models_loaded = (
        hasattr(request.app.state, "competency_analyzer")
        and request.app.state.competency_analyzer is not None
    )
    return HealthResponse(
        status="ok",
        database="connected" if models_loaded else "unknown",
        version="4.0.0"
    )
