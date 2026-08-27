"""
Nexus AI — Standalone Classification Endpoint
POST /api/classify — Runs the 4-tier cascade and returns ClassificationResult.
"""
import asyncio

from fastapi import APIRouter, Depends

from core.classifier import TicketClassifier
from api.models import TicketRequest, ClassificationResult
from api.deps import get_classifier

router = APIRouter(prefix="/api", tags=["modular"])


@router.post("/classify", response_model=ClassificationResult)
async def classify_ticket(
    ticket: TicketRequest,
    classifier: TicketClassifier = Depends(get_classifier),
) -> ClassificationResult:
    """
    Standalone classification endpoint.
    Runs the 4-tier cascade (novelty → fast path → LLM judge → escalation)
    and returns the structured classification result.

    Uses asyncio.to_thread() because classifier.classify() is synchronous
    and may trigger blocking LLM calls to Groq/Ollama.
    """
    result = await asyncio.to_thread(
        classifier.classify, ticket.title, ticket.description
    )
    return ClassificationResult(**result)
