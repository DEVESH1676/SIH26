from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/courses", tags=["courses"])

class EnrollRequest(BaseModel):
    course_id: str

MOCK_COURSES = [
    {
        "id": "c1",
        "title": "Introduction to Official Statistics",
        "description": "Foundational course on statistical systems in India.",
        "domain": "Statistics",
        "duration_hours": 5.0,
        "difficulty": "beginner",
        "skills": ["data_collection", "basics"],
        "tags": ["official", "mospi"],
        "source": "igot"
    },
    {
        "id": "c2",
        "title": "Advanced Data Visualization",
        "description": "Learn to visualize complex statistical data.",
        "domain": "Data Science",
        "duration_hours": 10.0,
        "difficulty": "advanced",
        "skills": ["visualization", "python", "d3"],
        "tags": ["data", "advanced"],
        "source": "tpac"
    }
]

@router.get("")
async def get_courses(domain: str = None, source: str = None, search: str = None):
    # In a real scenario, this would query ChromaDB or the SQL DB.
    # We return mock courses for the frontend to render.
    courses = MOCK_COURSES
    if domain and domain != "all":
        courses = [c for c in courses if c["domain"].lower() == domain.lower()]
    if search:
        courses = [c for c in courses if search.lower() in c["title"].lower()]
    return courses

@router.post("/enroll")
async def enroll_course(req: EnrollRequest):
    return {"status": "success", "message": f"Successfully enrolled in course {req.course_id}"}

@router.get("/enrolled")
async def get_enrolled_courses():
    # Mock enrolled courses
    return [MOCK_COURSES[0]]
