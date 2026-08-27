"""
Nexus AI — Health Check Endpoint
GET /api/health — Returns API status, loaded models, and available categories.
"""
from fastapi import APIRouter, Request

import config
from api.models import HealthResponse

router = APIRouter(prefix="/api", tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health_check(request: Request) -> HealthResponse:
    """Returns API health status and loaded model information."""
    models_loaded = (
        hasattr(request.app.state, "classifier")
        and request.app.state.classifier is not None
    )
    return HealthResponse(
        status="ok",
        models_loaded=models_loaded,
        version="4.0.0",
        categories=config.CATEGORIES,
    )
