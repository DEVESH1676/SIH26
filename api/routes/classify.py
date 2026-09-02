"""
MoSPI AI Learning Platform — Competency Analysis Endpoint
POST /api/analyze-profile — Extracts current skills and identifies missing skill gaps.
"""
import asyncio
from fastapi import APIRouter, Depends

from core.classifier import CompetencyAnalyzer
from api.models import LearnerProfileRequest, LearnerProfileResponse
from api.deps import get_analyzer

router = APIRouter(prefix="/api", tags=["competency"])


@router.post("/analyze-profile", response_model=LearnerProfileResponse)
async def analyze_profile(
    profile: LearnerProfileRequest,
    analyzer: CompetencyAnalyzer = Depends(get_analyzer),
) -> LearnerProfileResponse:
    """
    Analyze official's profile text and designation to identify competency gaps.
    """
    result = await asyncio.to_thread(
        analyzer.analyze_profile, profile.designation, profile.profile_text
    )
    return LearnerProfileResponse(**result)
