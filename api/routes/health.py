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
        hasattr(request.app.state, "analyzer")
        and request.app.state.analyzer is not None
    )
    return HealthResponse(
        status="ok",
        models_loaded=models_loaded,
        version="4.0.0",
        domain="MoSPI AI Learning Platform",
    )
