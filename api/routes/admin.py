"""
Admin & HR Directorate API Routes
Provides org-wide competency analytics and workforce data.
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any

from core.auth import require_role

router = APIRouter()

@router.get("/overview")
@require_role("admin")
async def get_admin_overview() -> Dict[str, Any]:
    """
    Returns high-level statistics on workforce competencies.
    """
    # Mock data for MVP
    return {
        "status": "success",
        "data": {
            "total_learners": 1500,
            "top_skill_gaps": [
                {"skill": "FUNC-003: Big Data Analytics", "count": 450},
                {"skill": "FUNC-001: Data Privacy (DPDP)", "count": 320},
                {"skill": "STAT-002: Index Numbers", "count": 210}
            ],
            "training_hours_completed": 12500,
            "average_competency_score": 7.2
        }
    }

@router.get("/workforce")
@require_role("admin")
async def get_workforce_data() -> Dict[str, Any]:
    """
    Returns detailed workforce competency distribution.
    """
    return {
        "status": "success",
        "data": {
            "departments": ["ISS", "SSS", "NSSTA"],
            "competency_distribution": {
                "Domain": {"Beginner": 200, "Intermediate": 500, "Advanced": 800},
                "Functional": {"Beginner": 600, "Intermediate": 600, "Advanced": 300},
                "Behavioral": {"Foundation": 100, "Proficient": 900, "Advanced": 500}
            }
        }
    }
