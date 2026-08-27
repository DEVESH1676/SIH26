"""
Nexus AI — Master Pipeline Endpoints
POST /api/pipeline/run    — Full pipeline, non-streaming (returns PipelineResponse)
GET  /api/pipeline/stream — Full pipeline, SSE streaming (yields ServerSentEvent)
"""
import asyncio
import time
import json
import logging
from collections.abc import AsyncIterable

from fastapi import APIRouter, Query, Request
from fastapi.sse import EventSourceResponse, ServerSentEvent

import config
from api.models import (
    TicketRequest, PipelineResponse, PipelineStatusEvent,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])


def _determine_decision_mode(
    triage_result: dict,
    judge_result: dict | None,
    confidence: float,
) -> str:
    """
    Derive decision_mode per CONTEXT.md escalation formatting rules.
    Returns: "auto_resolve" | "escalate" | "clarify"
    """
    if triage_result.get("escalate"):
        return "escalate"
    if confidence < 0.75 and judge_result is None:
        return "clarify"
    if judge_result and not judge_result.get("auto_resolve_allowed", True):
        return "escalate"
    return "auto_resolve"


def _run_pipeline_sync(
    request: Request,
    title: str,
    description: str,
    enable_resolution: bool,
) -> dict:
    """
    Synchronous pipeline execution — mirrors app.py run_full_pipeline() exactly.
    The 7-step chain: classify → triage → rag → rank → resolve → judge → automate.
    """
    state = request.app.state
    start_time = time.time()

    # Step 1: Classification
    classification = state.classifier.classify(title, description)

    # Step 2: Triage
    ticket = {"title": title, "description": description}
    triage_result = state.triage_agent.run(ticket, classification)

    # Step 3: RAG Retrieval
    rag_result = state.rag_engine.suggest_resolution(title, description)

    # Step 4: Rank chunks for resolution agent
    query_embedding = state.rag_engine.embedding_model.encode(
        f"{title} {description}"
    ).tolist()
    raw_results = state.rag_engine.collection.query(
        query_embeddings=[query_embedding],
        n_results=6,
        include=["documents", "metadatas", "distances"],
    )
    ranked_chunks = state.rag_engine._rank_retrieved_chunks(raw_results)[:3]

    resolution_result = None
    judge_result = None
    automation_result = None

    if enable_resolution:
        # Step 5: Resolution Agent
        resolution_result = state.resolution_agent.run(ticket, ranked_chunks)

        # Step 6: Judge
        resolution_text = "\n".join(
            resolution_result.get("resolution_steps", [])
        )
        judge_result = state.judge.judge(
            {
                "title": title,
                "description": description,
                "category": classification.get("category", "Unknown"),
            },
            resolution_text,
        )

        # Step 7: Automation Discovery
        automation_result = state.automation_agent.run(
            {
                "title": title,
                "description": description,
                "category": classification.get("category", "Unknown"),
                "resolution": resolution_text,
            }
        )
    else:
        # Still run automation check without resolution
        automation_result = state.automation_agent.run(
            {
                "title": title,
                "description": description,
                "category": classification.get("category", "Unknown"),
                "resolution": "",
            }
        )

    elapsed = round(time.time() - start_time, 2)
    decision_mode = _determine_decision_mode(
        triage_result, judge_result, classification.get("confidence", 0)
    )
    llm_provider = (
        f"Groq/{config.GROQ_MODEL}"
        if config.USE_GROQ
        else f"Ollama/{config.OLLAMA_MODEL}"
    )

    return {
        "decision_mode": decision_mode,
        "classification": classification,
        "triage": triage_result,
        "rag": rag_result,
        "resolution": resolution_result,
        "judge": judge_result,
        "automation": automation_result,
        "metadata": {
            "elapsed_seconds": elapsed,
            "llm_provider": llm_provider,
            "embedding_model": config.EMBEDDING_MODEL_NAME,
            "enable_resolution": enable_resolution,
        },
    }


# ──────────────────────────────────────────────────────────────
# POST /api/pipeline/run — Non-streaming full pipeline
# ──────────────────────────────────────────────────────────────
@router.post("/run", response_model=PipelineResponse)
async def run_pipeline(
    ticket: TicketRequest,
    request: Request,
) -> PipelineResponse:
    """
    Master Orchestrator — Full pipeline, non-streaming.
    Runs the entire 7-step intelligence cascade and returns a single PipelineResponse.
    Always returns 200 OK — decision_mode field indicates auto_resolve/escalate/clarify.
    """
    result = await asyncio.to_thread(
        _run_pipeline_sync,
        request,
        ticket.title,
        ticket.description,
        ticket.enable_resolution,
    )
    return PipelineResponse(**result)


# ──────────────────────────────────────────────────────────────
# Master SSE Streaming Logic
# ──────────────────────────────────────────────────────────────
async def _stream_pipeline_core(
    request: Request,
    title: str,
    description: str,
    enable_resolution: bool,
) -> AsyncIterable[ServerSentEvent]:
    """Shared SSE generator for both GET and POST endpoints."""
    state = request.app.state
    
    try:
        # Step 1: Classification
        yield ServerSentEvent(
            data=PipelineStatusEvent(
                stage="classifying",
                message="Extracting semantic embeddings...",
                progress=0.0,
            ).model_dump_json(),
            event="status",
        )
        classification = await asyncio.to_thread(
            state.classifier.classify, title, description
        )
        yield ServerSentEvent(
            data=json.dumps({"stage": "classified", "type": "classification", "payload": classification}),
            event="result",
        )

        # Step 2: Triage
        yield ServerSentEvent(
            data=PipelineStatusEvent(
                stage="triaging",
                message="Triage agent routing...",
                progress=0.15,
            ).model_dump_json(),
            event="status",
        )
        ticket_data = {"title": title, "description": description}
        triage_result = await asyncio.to_thread(
            state.triage_agent.run, ticket_data, classification
        )
        yield ServerSentEvent(
            data=json.dumps({"stage": "triaged", "type": "triage", "payload": triage_result}),
            event="result",
        )

        # Step 3: RAG Retrieval
        yield ServerSentEvent(
            data=PipelineStatusEvent(
                stage="retrieving",
                message="Retrieving & ranking historical evidence...",
                progress=0.30,
            ).model_dump_json(),
            event="status",
        )
        rag_result = await asyncio.to_thread(
            state.rag_engine.suggest_resolution, title, description
        )

        # Step 4: Rank chunks
        query_embedding = await asyncio.to_thread(
            state.rag_engine.embedding_model.encode, f"{title} {description}"
        )
        raw_results = await asyncio.to_thread(
            lambda: state.rag_engine.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=6,
                include=["documents", "metadatas", "distances"],
            )
        )
        ranked_chunks = state.rag_engine._rank_retrieved_chunks(raw_results)[:3]
        yield ServerSentEvent(
            data=json.dumps({"stage": "retrieved", "type": "rag", "payload": rag_result}),
            event="result",
        )

        resolution_result = None
        judge_result = None
        automation_result = None

        if enable_resolution:
            # Step 5: Resolution Agent
            yield ServerSentEvent(
                data=PipelineStatusEvent(
                    stage="resolving",
                    message="Resolution agent generating fix...",
                    progress=0.50,
                ).model_dump_json(),
                event="status",
            )
            resolution_result = await asyncio.to_thread(
                state.resolution_agent.run, ticket_data, ranked_chunks
            )
            yield ServerSentEvent(
                data=json.dumps({"stage": "resolved", "type": "resolution", "payload": resolution_result}),
                event="result",
            )

            # Step 6: Judge
            yield ServerSentEvent(
                data=PipelineStatusEvent(
                    stage="judging",
                    message="Quality judge evaluating resolution...",
                    progress=0.70,
                ).model_dump_json(),
                event="status",
            )
            resolution_text = "\n".join(
                resolution_result.get("resolution_steps", [])
            )
            judge_result = await asyncio.to_thread(
                state.judge.judge,
                {
                    "title": title,
                    "description": description,
                    "category": classification.get("category", "Unknown"),
                },
                resolution_text,
            )
            yield ServerSentEvent(
                data=json.dumps({"stage": "judged", "type": "judge", "payload": judge_result}),
                event="result",
            )

            # Step 7: Automation Discovery
            yield ServerSentEvent(
                data=PipelineStatusEvent(
                    stage="automating",
                    message="Scanning for automation patterns...",
                    progress=0.85,
                ).model_dump_json(),
                event="status",
            )
            automation_result = await asyncio.to_thread(
                state.automation_agent.run,
                {
                    "title": title,
                    "description": description,
                    "category": classification.get("category", "Unknown"),
                    "resolution": resolution_text,
                },
            )
            yield ServerSentEvent(
                data=json.dumps({"stage": "automated", "type": "automation", "payload": automation_result}),
                event="result",
            )
        else:
            automation_result = await asyncio.to_thread(
                state.automation_agent.run,
                {
                    "title": title,
                    "description": description,
                    "category": classification.get("category", "Unknown"),
                    "resolution": "",
                },
            )

        # Final: Complete
        decision_mode = _determine_decision_mode(
            triage_result, judge_result, classification.get("confidence", 0)
        )
        llm_provider = (
            f"Groq/{config.GROQ_MODEL}"
            if config.USE_GROQ
            else f"Ollama/{config.OLLAMA_MODEL}"
        )

        final_response = {
            "decision_mode": decision_mode,
            "classification": classification,
            "triage": triage_result,
            "rag": rag_result,
            "resolution": resolution_result,
            "judge": judge_result,
            "automation": automation_result,
            "metadata": {
                "llm_provider": llm_provider,
                "embedding_model": config.EMBEDDING_MODEL_NAME,
                "enable_resolution": enable_resolution,
            },
        }

        yield ServerSentEvent(
            data=PipelineStatusEvent(
                stage="complete", message="Pipeline complete", progress=1.0
            ).model_dump_json(),
            event="status",
        )
        yield ServerSentEvent(data=json.dumps(final_response), event="done")

    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}", exc_info=True)
        yield ServerSentEvent(
            data=json.dumps({"stage": "error", "message": f"Pipeline failure: {str(e)}"}),
            event="status",
        )


@router.get("/stream", response_class=EventSourceResponse)
async def stream_pipeline_get(
    request: Request,
    title: str = Query(..., min_length=3),
    description: str = Query(..., min_length=10),
    enable_resolution: bool = Query(True),
) -> AsyncIterable[ServerSentEvent]:
    """Master Orchestrator — SSE streaming pipeline (GET)."""
    async for event in _stream_pipeline_core(request, title, description, enable_resolution):
        yield event


@router.post("/stream", response_class=EventSourceResponse)
async def stream_pipeline_post(
    ticket: TicketRequest,
    request: Request,
) -> AsyncIterable[ServerSentEvent]:
    """Master Orchestrator — SSE streaming pipeline (POST)."""
    async for event in _stream_pipeline_core(
        request, ticket.title, ticket.description, ticket.enable_resolution
    ):
        yield event
