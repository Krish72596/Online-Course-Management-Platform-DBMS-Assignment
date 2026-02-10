from sqlalchemy.orm import Session
from app.models.quiz import Quiz, QuizQuestion
from app.models.course import Course


def create_quiz(db: Session, course_id: int, quiz_data: dict):
    """Create a new quiz for a course"""
    quiz = Quiz(
        course_id=course_id,
        title=quiz_data.get('title', 'Final Test'),
        description=quiz_data.get('description'),
        max_attempts=quiz_data.get('max_attempts', 1),
        passing_score=quiz_data.get('passing_score', 70)
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz


def get_quiz_by_id(db: Session, quiz_id: int):
    """Get a quiz by ID"""
    return db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()


def get_quiz_by_course(db: Session, course_id: int):
    """Get quiz for a specific course"""
    return db.query(Quiz).filter(Quiz.course_id == course_id).first()


def add_question(db: Session, quiz_id: int, question_data: dict):
    """Add a question to a quiz"""
    # Get the next order number
    max_order = db.query(QuizQuestion).filter(
        QuizQuestion.quiz_id == quiz_id
    ).with_entities(QuizQuestion.order).order_by(QuizQuestion.order.desc()).first()
    
    next_order = (max_order[0] + 1) if max_order else 1
    
    question = QuizQuestion(
        quiz_id=quiz_id,
        question_text=question_data.get('question_text'),
        question_type=question_data.get('question_type', 'multiple_choice'),
        option_a=question_data.get('option_a'),
        option_b=question_data.get('option_b'),
        option_c=question_data.get('option_c'),
        option_d=question_data.get('option_d'),
        correct_answer=question_data.get('correct_answer'),
        explanation=question_data.get('explanation'),
        order=next_order
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_questions(db: Session, quiz_id: int):
    """Get all questions for a quiz ordered by order field"""
    return db.query(QuizQuestion).filter(
        QuizQuestion.quiz_id == quiz_id
    ).order_by(QuizQuestion.order).all()


def update_question(db: Session, question_id: int, question_data: dict):
    """Update a quiz question"""
    question = db.query(QuizQuestion).filter(
        QuizQuestion.question_id == question_id
    ).first()
    
    if not question:
        return None
    
    for key, value in question_data.items():
        if hasattr(question, key):
            setattr(question, key, value)
    
    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question_id: int):
    """Delete a quiz question"""
    question = db.query(QuizQuestion).filter(
        QuizQuestion.question_id == question_id
    ).first()
    
    if question:
        db.delete(question)
        db.commit()
        return True
    return False


def update_answer_key(db: Session, course_id: int, answer_key: str):
    """Update the answer key for a course"""
    course = db.query(Course).filter(Course.course_id == course_id).first()
    
    if not course:
        return None
    
    course.quiz_answer_key = answer_key
    db.commit()
    db.refresh(course)
    return course
