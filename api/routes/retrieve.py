"""
MoSPI AI Learning Platform — Course Recommendation Endpoint
POST /api/recommend-pathway — Queries course catalog and generates a personalized learning pathway.
"""
import asyncio

from fastapi import APIRouter, Depends

from api.deps import get_recommender
from api.models import PathwayRequest, PathwayResponse
from core.rag import CourseRecommender

router = APIRouter(prefix="/api", tags=["pathway"])


@router.post("/recommend-pathway", response_model=PathwayResponse)
async def recommend_pathway(
    req: PathwayRequest,
    recommender: CourseRecommender = Depends(get_recommender),
) -> PathwayResponse:
    """
    Recommend iGOT courses and build a custom learning pathway based on skill gaps.
    """
    result = await asyncio.to_thread(
        recommender.suggest_courses, req.skill_gaps
    )
    return PathwayResponse(**result)
