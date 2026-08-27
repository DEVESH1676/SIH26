"""
Nexus AI — Execution History Endpoint
GET /api/history — Returns all past pipeline runs from feedback.db.
"""
from fastapi import APIRouter, Request
from core.feedback import FeedbackStore

router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history")
def get_history(request: Request):
    """Retrieves all pipeline run records from the feedback database."""
    # We use the store instance attached to app state
    store: FeedbackStore = request.app.state.feedback_store
    rows = store.get_all()
    
    # Return as a simple list of dicts
    return {"history": rows}
