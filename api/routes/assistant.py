"""
MoSPI AI Learning Platform - Virtual Assistant Endpoint
POST /api/assistant - Chat with the AI assistant
"""
from fastapi import APIRouter, Request, HTTPException
from api.models import AssistantRequest, AssistantResponse

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


@router.post("", response_model=AssistantResponse)
async def chat_with_assistant(req: AssistantRequest, request: Request):
    """Chat with the virtual assistant."""
    assistant = getattr(request.app.state, "virtual_assistant", None)

    if assistant:
        try:
            if req.language and req.language != "en":
                result = await assistant.respond_multilingual(
                    user_message=req.message,
                    language=req.language,
                    user_context=req.user_context
                )
            else:
                result = await assistant.respond(
                    user_message=req.message,
                    user_context=req.user_context
                )
            return AssistantResponse(**result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Fallback: return helpful response without LLM
    response_map = {
        "help": "I can help you with course recommendations, skill gap analysis, quiz preparation, and navigation.",
        "courses": "Browse our catalog at /courses to find iGOT Karmayogi micro-learning courses and NSSTA TPAC programs.",
        "quiz": "Take a quiz at /quiz to assess your competency. You can also generate custom quizzes from documents.",
        "gaps": "View your skill gaps at /dashboard. These are identified through AI-powered competency analysis.",
        "analytics": "Check your progress at /analytics for detailed learning statistics and competency scores.",
    }

    lower_msg = req.message.lower()
    for key, response in response_map.items():
        if key in lower_msg:
            return AssistantResponse(
                response=response,
                suggested_actions=[
                    {"label": "Browse Courses", "action": "/courses"},
                    {"label": "View Analytics", "action": "/analytics"},
                ],
                related_resources=[],
                intent="general"
            )

    return AssistantResponse(
        response=f"I'm here to help! You can ask me about courses, quizzes, your skill gaps, or analytics.",
        suggested_actions=[
            {"label": "Browse Courses", "action": "/courses"},
            {"label": "Take a Quiz", "action": "/quiz"},
            {"label": "View Analytics", "action": "/analytics"},
        ],
        related_resources=[],
        intent="greeting"
    )
