"""
Nexus AI — Standalone RAG Retrieval Endpoint
POST /api/retrieve — Runs multi-hop semantic retrieval and returns RAGResult.
"""
import asyncio

from fastapi import APIRouter, Depends

from core.rag import ResolutionEngine
from api.models import TicketRequest, RAGResult
from api.deps import get_rag_engine

router = APIRouter(prefix="/api", tags=["modular"])


@router.post("/retrieve", response_model=RAGResult)
async def retrieve_context(
    ticket: TicketRequest,
    rag_engine: ResolutionEngine = Depends(get_rag_engine),
) -> RAGResult:
    """
    Standalone RAG retrieval endpoint.
    Performs multi-hop semantic retrieval and returns ranked evidence
    with an LLM-generated resolution suggestion.

    Uses asyncio.to_thread() because rag_engine.suggest_resolution()
    makes blocking HTTP calls to Groq/Ollama.
    """
    result = await asyncio.to_thread(
        rag_engine.suggest_resolution, ticket.title, ticket.description
    )
    return RAGResult(**result)
