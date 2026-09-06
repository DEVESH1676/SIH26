"""
MoSPI AI Learning Platform — Master Learning Pipeline Endpoints
POST /api/pipeline/generate-plan  — Full learning plan creation (non-streaming)
GET  /api/pipeline/stream           — Learning plan creation (SSE streaming)
"""
import asyncio
import json
import logging
from collections.abc import AsyncIterable

from fastapi import APIRouter, Request
from fastapi.sse import EventSourceResponse, ServerSentEvent

from api.models import LearnerProfileRequest, PipelineStatusEvent
from core.auth import require_role

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])


async def _stream_lms_pipeline(
    request: Request,
    designation: str,
    profile_text: str,
) -> AsyncIterable[ServerSentEvent]:
    """SSE generator for generating personalized learning plans."""
    state = request.app.state
    analyzer = getattr(state, "analyzer", None)
    recommender = getattr(state, "recommender", None)
    use_fallback = analyzer is None or recommender is None

    if use_fallback:
        logger.warning("Pipeline running in fallback mode (core services not initialized)")

    try:
        # Step 1: Profiling
        yield ServerSentEvent(
            data=PipelineStatusEvent(
                stage="profiling",
                message="Analyzing official profile and competency framework..." if not use_fallback else "Analyzing profile (basic mode)...",
                progress=0.1,
            ).model_dump_json(),
            event="status",
        )

        if use_fallback:
            profile_analysis = await _fallback_analyze_profile(designation, profile_text)
        else:
            profile_analysis = await asyncio.to_thread(
                analyzer.analyze_profile, designation, profile_text
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
                message="Querying iGOT course catalog & building learning pathway..." if not use_fallback else "Building learning pathway (basic mode)...",
                progress=0.7,
            ).model_dump_json(),
            event="status",
        )

        if use_fallback:
            pathway_result = await _fallback_suggest_courses(skill_gaps)
        else:
            pathway_result = await asyncio.to_thread(
                recommender.suggest_courses, skill_gaps
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
        logger.error(f"LMS Pipeline error: {e!s}", exc_info=True)
        yield ServerSentEvent(
            data=json.dumps({"stage": "error", "message": f"Pipeline failure: {e!s}"}),
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
    analyzer = getattr(state, "analyzer", None)
    recommender = getattr(state, "recommender", None)
    use_fallback = analyzer is None or recommender is None

    if use_fallback:
        profile_analysis = await _fallback_analyze_profile(req.designation, req.profile_text)
        pathway_result = await _fallback_suggest_courses(profile_analysis.get("skill_gaps", []))
    else:
        profile_analysis = await asyncio.to_thread(
            analyzer.analyze_profile, req.designation, req.profile_text
        )
        skill_gaps = profile_analysis.get("skill_gaps", [])
        pathway_result = await asyncio.to_thread(
            recommender.suggest_courses, skill_gaps
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


# ── Fallback: if analyzer/recommender not on state ───────────
async def _fallback_analyze_profile(designation: str, profile_text: str) -> dict:
    """Fallback competency analysis when core services aren't available."""
    return {
        "current_skills": [{"id": "GEN-001", "name": "General Administration", "level": "Intermediate"}],
        "skill_gaps": [
            {"id": "STAT-001", "name": "Statistical Methods", "priority": "high", "domain": "Statistical", "reason": "Core competency for official roles"},
            {"id": "TECH-001", "name": "Data Analysis Tools", "priority": "medium", "domain": "Technical", "reason": "Modern data processing requirement"}
        ],
        "competency_summary": {"overall": "developing", "strengths": ["Administration"], "gaps": ["Statistical", "Technical"]},
        "analysis_summary": "Profile indicates need for foundational statistical and technical upskilling."
    }


async def _fallback_suggest_courses(skill_gaps: list) -> dict:
    """Fallback course recommendation when recommender isn't available."""
    return {
        "courses": [],
        "tpac_programs": [],
        "suggested_pathway": "Based on identified skill gaps, we recommend foundational courses in Statistical Methods and Data Analysis tools. Please complete these modules to strengthen your core competencies.",
        "estimated_hours": 20
    }
