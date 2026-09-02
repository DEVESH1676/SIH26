"""
MoSPI AI Learning Platform — Master Learning Pipeline Endpoints
POST /api/pipeline/generate-plan  — Full learning plan creation (non-streaming)
GET  /api/pipeline/stream           — Learning plan creation (SSE streaming)
"""
import asyncio
import time
import json
import logging
from collections.abc import AsyncIterable

from fastapi import APIRouter, Query, Request
from fastapi.sse import EventSourceResponse, ServerSentEvent


from core.auth import require_role
from api.models import (
    LearnerProfileRequest, PipelineStatusEvent
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])


async def _stream_lms_pipeline(
    request: Request,
    designation: str,
    profile_text: str,
) -> AsyncIterable[ServerSentEvent]:
    """SSE generator for generating personalized learning plans."""
    state = request.app.state
    
    try:
        # Step 1: Profiling
        yield ServerSentEvent(
            data=PipelineStatusEvent(
                stage="profiling",
                message="Analyzing official profile and competency framework...",
                progress=0.1,
            ).model_dump_json(),
            event="status",
        )
        
        profile_analysis = await asyncio.to_thread(
            state.analyzer.analyze_profile, designation, profile_text
        )
        
        yield ServerSentEvent(
            data=json.dumps({"stage": "profiled", "type": "profile", "payload": profile_analysis}),
            event="result",
        )

        # Step 2: Extracting Gaps
        yield ServerSentEvent(
            data=PipelineStatusEvent(
                stage="identifying_gaps",
                message="Extracted competencies & identifying skill gaps...",
                progress=0.4,
            ).model_dump_json(),
            event="status",
        )
        
        skill_gaps = profile_analysis.get("skill_gaps", [])

        # Step 3: Course Matching & Pathway Building
        yield ServerSentEvent(
            data=PipelineStatusEvent(
                stage="matching_courses",
                message="Querying iGOT course catalog & building learning pathway...",
                progress=0.7,
            ).model_dump_json(),
            event="status",
        )
        
        pathway_result = await asyncio.to_thread(
            state.recommender.suggest_courses, skill_gaps
        )
        
        yield ServerSentEvent(
            data=json.dumps({"stage": "pathway_built", "type": "pathway", "payload": pathway_result}),
            event="result",
        )

        # Step 4: Complete
        final_response = {
            "profile": profile_analysis,
            "pathway": pathway_result,
            "status": "success"
        }

        yield ServerSentEvent(
            data=PipelineStatusEvent(
                stage="complete", message="Learning plan successfully generated!", progress=1.0
            ).model_dump_json(),
            event="status",
        )
        yield ServerSentEvent(data=json.dumps(final_response), event="done")

    except Exception as e:
        logger.error(f"LMS Pipeline error: {str(e)}", exc_info=True)
        yield ServerSentEvent(
            data=json.dumps({"stage": "error", "message": f"Pipeline failure: {str(e)}"}),
            event="status",
        )


@router.post("/generate-plan")
@require_role("learner")
async def generate_plan_post(
    req: LearnerProfileRequest,
    request: Request,
):
    """Non-streaming endpoint to generate complete learning plan."""
    state = request.app.state
    profile_analysis = await asyncio.to_thread(
        state.analyzer.analyze_profile, req.designation, req.profile_text
    )
    skill_gaps = profile_analysis.get("skill_gaps", [])
    pathway_result = await asyncio.to_thread(
        state.recommender.suggest_courses, skill_gaps
    )
    return {
        "profile": profile_analysis,
        "pathway": pathway_result,
        "status": "success"
    }


@router.post("/stream", response_class=EventSourceResponse)
@require_role("learner")
async def stream_pipeline_post(
    req: LearnerProfileRequest,
    request: Request,
) -> AsyncIterable[ServerSentEvent]:
    """SSE streaming endpoint (POST)."""
    async for event in _stream_lms_pipeline(request, req.designation, req.profile_text):
        yield event
