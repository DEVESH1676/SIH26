import json
import sqlite3
import os
import uuid
from fastapi import APIRouter, Request, HTTPException, UploadFile, File, Form
from api.models import QuizCreate, QuizAttemptRequest, QuizResponse, QuizResult
from config.settings import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/quiz", tags=["quiz"])


def _get_engine(request: Request):
    """Get quiz engine with fallback."""
    engine = getattr(request.app.state, "quiz_engine", None)
    if engine is None:
        from core.quiz_engine import QuizEngine
        engine = QuizEngine()
        request.app.state.quiz_engine = engine
    return engine


@router.post("/generate", response_model=dict)
async def generate_quiz(req: QuizCreate, request: Request):
    engine = _get_engine(request)
    try:
        result = await engine.generate_mcqs(
            document_text=req.source_text,
            num_questions=req.num_questions,
            difficulty=req.difficulty,
            domain=req.domain,
        )
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {e}")


@router.post("/upload", response_model=dict)
async def upload_quiz_file(
    request: Request,
    file: UploadFile = File(...),
    num_questions: int = Form(5),
    difficulty: str = Form("intermediate")
):
    engine = _get_engine(request)

    # Save file temporarily
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    file_extension = file.filename.split(".")[-1]

    try:
        result = await engine.generate_from_file(
            file_path=file_path,
            file_type=file_extension,
            num_questions=num_questions,
            difficulty=difficulty,
        )
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")
    finally:
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/list")
async def list_quizzes(request: Request):
    conn = sqlite3.connect(settings.sqlite_path)
    conn.row_factory = sqlite3.Row
    quizzes = conn.execute("SELECT * FROM quizzes ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(q) for q in quizzes]


@router.get("/{quiz_id}")
async def get_quiz(quiz_id: str, request: Request):
    conn = sqlite3.connect(settings.sqlite_path)
    conn.row_factory = sqlite3.Row

    # Get quiz metadata
    quiz = conn.execute("SELECT * FROM quizzes WHERE quiz_id = ?", (quiz_id,)).fetchone()
    if not quiz:
        conn.close()
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Get quiz questions
    questions_raw = conn.execute(
        "SELECT id, question, options, correct_answer, explanation, difficulty, category FROM quiz_questions WHERE quiz_id = ?",
        (quiz_id,)
    ).fetchall()
    conn.close()

    # Build question list
    questions = []
    for q in questions_raw:
        questions.append({
            "id": str(q[0]),
            "question": q[1],
            "options": json.loads(q[2]) if isinstance(q[2], str) else q[2],
            "correct_answer": int(q[3]),
            "explanation": q[4] or "",
            "difficulty": q[5] or "intermediate",
            "category": q[6] or "general"
        })

    return {
        "quiz_id": quiz["quiz_id"],
        "quiz_title": quiz["title"],
        "questions": questions,
        "source": "db"
    }


@router.post("/attempt", response_model=QuizResult)
async def submit_quiz_attempt(attempt: QuizAttemptRequest, request: Request):
    conn = sqlite3.connect(settings.sqlite_path)
    conn.row_factory = sqlite3.Row

    # Get quiz
    quiz = conn.execute("SELECT * FROM quizzes WHERE quiz_id = ?", (attempt.quiz_id,)).fetchone()
    if not quiz:
        conn.close()
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Get questions
    questions_raw = conn.execute(
        "SELECT id, question, options, correct_answer, explanation, difficulty, category FROM quiz_questions WHERE quiz_id = ?",
        (attempt.quiz_id,)
    ).fetchall()
    conn.close()

    # Build questions list
    questions = []
    for q in questions_raw:
        questions.append({
            "id": str(q[0]),
            "question": q[1],
            "options": json.loads(q[2]) if isinstance(q[2], str) else q[2],
            "correct_answer": int(q[3]),
            "explanation": q[4] or "",
            "difficulty": q[5] or "intermediate",
            "category": q[6] or "general"
        })

    # Calculate score
    score = 0
    total = len(questions)
    results = []
    for q in questions:
        selected = attempt.answers.get(q["id"], -1)
        is_correct = selected == q["correct_answer"]
        if is_correct:
            score += 1
        results.append({
            "question_id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "selected": selected,
            "correct_answer": q["correct_answer"],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })

    percentage = round((score / total) * 100, 1) if total > 0 else 0

    return QuizResult(
        score=score,
        total=total,
        percentage=percentage,
        passed=percentage >= 60,
        results=results
    )
