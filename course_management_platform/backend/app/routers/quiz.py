from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.services.quiz_service import (
    create_or_get_quiz_service,
    add_question_service,
    get_quiz_questions_service,
    get_quiz_by_course_service,
    update_answer_key_service,
    delete_question_service
)

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"]
)

# Schemas
class QuestionCreate(BaseModel):
    question_text: str
    question_type: str = "multiple_choice"
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_answer: str
    explanation: Optional[str] = None


class AnswerKeyUpdate(BaseModel):
    quiz_answer_key: str


# Routes

@router.post("/course/{course_id}")
def create_quiz_for_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    """Create or get a quiz for a course"""
    return create_or_get_quiz_service(db, course_id)


@router.get("/{quiz_id}/questions")
def get_quiz_questions(
    quiz_id: int,
    db: Session = Depends(get_db)
):
    """Get all questions for a specific quiz"""
    return get_quiz_questions_service(db, quiz_id)


@router.post("/{quiz_id}/questions")
def add_quiz_question(
    quiz_id: int,
    question: QuestionCreate,
    db: Session = Depends(get_db)
):
    """Add a question to a quiz"""
    return add_question_service(db, quiz_id, question.dict())


@router.get("/course/{course_id}")
def get_course_quiz(
    course_id: int,
    db: Session = Depends(get_db)
):
    """Get quiz for a specific course"""
    return get_quiz_by_course_service(db, course_id)


@router.delete("/questions/{question_id}")
def delete_quiz_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Delete a question from a quiz"""
    return delete_question_service(db, question_id)


@router.put("/courses/{course_id}/answer-key")
def update_course_answer_key(
    course_id: int,
    payload: AnswerKeyUpdate,
    db: Session = Depends(get_db)
):
    """Update answer key for a course"""
    return update_answer_key_service(db, course_id, payload.quiz_answer_key)
