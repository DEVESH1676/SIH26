"""
MoSPI AI Learning Platform — Assessment & Evaluation Endpoints
POST /api/assessment/generate-mcq  — Generates JSON MCQs from document text.
POST /api/assessment/evaluate-answer — Evaluates learner's subjective answer.
"""
import asyncio
from fastapi import APIRouter, Depends

from core.rag import QuizGenerator
from core.judge import SubjectiveAssessor
from api.models import (
    QuizRequest, QuizResponse, MCQQuestion,
    SubjectiveAnswerRequest, SubjectiveAnswerResponse,
    QuizAttemptRequest, QuizAttemptResponse
)
from api.deps import get_quiz_generator, get_subjective_assessor

router = APIRouter(prefix="/api/assessment", tags=["assessment"])


@router.post("/generate-mcq", response_model=QuizResponse)
async def generate_mcq(
    req: QuizRequest,
    generator: QuizGenerator = Depends(get_quiz_generator),
) -> QuizResponse:
    """
    Generate multiple-choice questions from uploaded learning material.
    """
    result = await asyncio.to_thread(
        generator.generate_mcqs, req.document_text, req.num_questions
    )
    
    if result.get("status") == "success" and "data" in result:
        questions_data = result["data"].get("quiz", [])
        questions = []
        for i, q in enumerate(questions_data):
            questions.append(MCQQuestion(
                question_id=i+1,
                question=q.get("question", ""),
                options=q.get("options", []),
                correct_answer=q.get("correct_answer", ""),
                explanation=q.get("explanation", "")
            ))
        return QuizResponse(quiz_title="Generated Assessment", questions=questions)
    
    # Fallback/Error case
    return QuizResponse(quiz_title="Error Generating Quiz", questions=[])


@router.post("/evaluate-answer", response_model=SubjectiveAnswerResponse)
async def evaluate_answer(
    req: SubjectiveAnswerRequest,
    assessor: SubjectiveAssessor = Depends(get_subjective_assessor),
) -> SubjectiveAnswerResponse:
    """
    Evaluate learner's subjective answer to a conceptual question on Accuracy, Comprehension, and Completeness.
    """
    result = await asyncio.to_thread(
        assessor.evaluate_answer, req.question, req.expected_key_points, req.learner_answer
    )
    return SubjectiveAnswerResponse(**result)


@router.post("/parse-and-generate", response_model=QuizResponse)
async def parse_and_generate_mcq(
    file_path: str,
    num_questions: int = 5,
    generator: QuizGenerator = Depends(get_quiz_generator),
) -> QuizResponse:
    """
    Parse a document/media file and generate a quiz from it.
    """
    from core.parser import MediaParser
    parser = MediaParser()
    
    # In a real app this would accept an UploadFile, save it, and pass the path
    text_content = await asyncio.to_thread(parser.parse_file, file_path)
    
    result = await asyncio.to_thread(
        generator.generate_mcqs, text_content, num_questions
    )
    
    if result.get("status") == "success" and "data" in result:
        questions_data = result["data"].get("quiz", [])
        questions = []
        for i, q in enumerate(questions_data):
            questions.append(MCQQuestion(
                question_id=i+1,
                question=q.get("question", ""),
                options=q.get("options", []),
                correct_answer=q.get("correct_answer", ""),
                explanation=q.get("explanation", "")
            ))
        return QuizResponse(quiz_title="Generated Assessment", questions=questions)
        
    return QuizResponse(quiz_title="Error Generating Quiz", questions=[])


@router.post("/log-attempt", response_model=QuizAttemptResponse)
async def log_quiz_attempt(
    req: QuizAttemptRequest,
):
    """
    Log a learner's quiz attempt for tracking progress.
    """
    from core.feedback import ProgressStore
    store = ProgressStore()
    
    await asyncio.to_thread(
        store.log_event,
        learner_id=req.learner_id,
        event_type="quiz_attempt",
        quiz_id=req.quiz_id,
        score=req.score,
        event_data={"passed": req.passed}
    )
    
    store.close()
    return QuizAttemptResponse(status="success", message="Attempt logged successfully")
