from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories import quiz_repo
from app.models.course import Course


def create_or_get_quiz_service(db: Session, course_id: int):
    """Create a new quiz for a course or get existing one"""
    # Validate course exists
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if quiz already exists
    existing_quiz = quiz_repo.get_quiz_by_course(db, course_id)
    if existing_quiz:
        return existing_quiz
    
    # Create new quiz
    quiz_data = {
        'title': 'Final Test',
        'description': 'Final assessment quiz for this course',
        'max_attempts': 1,
        'passing_score': 70
    }
    return quiz_repo.create_quiz(db, course_id, quiz_data)


def add_question_service(db: Session, quiz_id: int, question_data: dict):
    """Add a question to a quiz"""
    # Validate quiz exists
    quiz = quiz_repo.get_quiz_by_id(db, quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Validate required fields
    if not question_data.get('question_text'):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Question text is required"
        )
    
    if not question_data.get('correct_answer'):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Correct answer is required"
        )
    
    return quiz_repo.add_question(db, quiz_id, question_data)


def get_quiz_questions_service(db: Session, quiz_id: int):
    """Get all questions for a quiz"""
    quiz = quiz_repo.get_quiz_by_id(db, quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    questions = quiz_repo.get_questions(db, quiz_id)
    return {
        'quiz_id': quiz.quiz_id,
        'course_id': quiz.course_id,
        'title': quiz.title,
        'description': quiz.description,
        'max_attempts': quiz.max_attempts,
        'passing_score': quiz.passing_score,
        'questions': [
            {
                'question_id': q.question_id,
                'question_text': q.question_text,
                'question_type': q.question_type,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'correct_answer': q.correct_answer,
                'explanation': q.explanation,
                'order': q.order
            }
            for q in questions
        ]
    }


def get_quiz_by_course_service(db: Session, course_id: int):
    """Get quiz for a course"""
    quiz = quiz_repo.get_quiz_by_course(db, course_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found for this course"
        )
    
    questions = quiz_repo.get_questions(db, quiz.quiz_id)
    return {
        'quiz_id': quiz.quiz_id,
        'course_id': quiz.course_id,
        'title': quiz.title,
        'description': quiz.description,
        'max_attempts': quiz.max_attempts,
        'passing_score': quiz.passing_score,
        'questions': [
            {
                'question_id': q.question_id,
                'question_text': q.question_text,
                'question_type': q.question_type,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'correct_answer': q.correct_answer,
                'explanation': q.explanation,
                'order': q.order
            }
            for q in questions
        ]
    }


def update_answer_key_service(db: Session, course_id: int, answer_key: str):
    """Update answer key for a course"""
    # Validate course exists
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    updated_course = quiz_repo.update_answer_key(db, course_id, answer_key)
    return {
        'course_id': updated_course.course_id,
        'quiz_answer_key': updated_course.quiz_answer_key
    }


def delete_question_service(db: Session, question_id: int):
    """Delete a question from a quiz"""
    if not quiz_repo.delete_question(db, question_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return {'message': 'Question deleted successfully'}
