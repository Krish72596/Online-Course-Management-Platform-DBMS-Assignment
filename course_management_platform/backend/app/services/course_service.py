from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories import course_repo
from app.repositories import quiz_repo

# UNIVERSITY SERVICES
def create_university_service(db: Session, payload):

    university = course_repo.create_university(
        db,
        payload.dict()
    )

    return university


def get_all_universities_service(db: Session):
    return course_repo.get_all_universities(db)

# COURSE SERVICES
def create_course_service(db: Session, payload):

    # Validate university if provided
    if payload.university_id:

        university = course_repo.get_university_by_id(
            db,
            payload.university_id
        )

        if not university:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="University not found"
            )

    course = course_repo.create_course(
        db,
        payload.dict()
    )

    return course


def get_all_courses_service(db: Session):
    return course_repo.get_approved_courses(db)


def create_instructor_course_service(db: Session, payload, instructor_user_id: int):
    """Create a course as an instructor with Pending approval status"""
    
    # Validate university if provided
    if payload.university_id:
        university = course_repo.get_university_by_id(
            db,
            payload.university_id
        )
        if not university:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="University not found"
            )
    
    # Prepare course data - exclude topics and quiz_questions
    course_data = payload.dict(exclude={'topics', 'quiz_questions'}, exclude_none=True)
    course_data['created_by'] = instructor_user_id
    course_data['approval_status'] = 'Pending'
    
    # Create the course
    course = course_repo.create_course(db, course_data)
    
    # Create topics and map them to course if provided
    if payload.topics:
        for topic in payload.topics:
            # Convert TopicCreate to dict if needed
            topic_data = topic.dict() if hasattr(topic, 'dict') else topic
            created_topic = course_repo.create_topic(db, topic_data)
            course_repo.map_topic_to_course(
                db,
                course.course_id,
                created_topic.topic_id,
                None
            )
    
    # Create quiz and questions if provided
    if payload.quiz_questions and len(payload.quiz_questions) > 0:
        # Create a Quiz row
        quiz_data = {
            'title': 'Final Assessment',
            'description': 'Final assessment quiz for ' + course.title,
            'max_attempts': 1,
            'passing_score': 70
        }
        quiz = quiz_repo.create_quiz(db, course.course_id, quiz_data)
        
        # Add all questions to the quiz
        for question in payload.quiz_questions:
            question_data = question.dict() if hasattr(question, 'dict') else question
            quiz_repo.add_question(db, quiz.quiz_id, question_data)
    
    # Create "Final Assessment" topic for the quiz (if quiz exists)
    if payload.quiz_questions and len(payload.quiz_questions) > 0:
        final_assessment_topic = course_repo.create_topic(
            db,
            {'name': 'Final Assessment', 'description': 'Take the final quiz to complete the course'}
        )
        course_repo.map_topic_to_course(
            db,
            course.course_id,
            final_assessment_topic.topic_id,
            None
        )
    
    return course


def get_instructor_pending_courses_service(db: Session, instructor_user_id: int):
    """Get pending courses created by specific instructor"""
    return course_repo.get_pending_courses_by_instructor(db, instructor_user_id)


def get_course_by_id_service(db: Session, course_id: int):

    course = course_repo.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


# TOPIC SERVICES
def create_topic_service(db: Session, payload):

    topic = course_repo.create_topic(
        db,
        payload.dict()
    )

    return topic


def get_all_topics_service(db: Session):
    return course_repo.get_all_topics(db)


# COURSE ↔ TOPIC MAPPING
def map_topic_to_course_service(
    db: Session,
    course_id: int,
    topic_id: int,
    sequence_order: int | None
):

    # Validate course
    course = course_repo.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Validate topic
    topic = course_repo.get_topic_by_id(db, topic_id)

    if not topic:
        raise HTTPException(
            status_code=404,
            detail="Topic not found"
        )

    # Prevent duplicate mapping
    existing_mappings = course_repo.get_topics_by_course(
        db,
        course_id
    )

    for m in existing_mappings:
        if m.topic_id == topic_id:
            raise HTTPException(
                status_code=400,
                detail="Topic already mapped to course"
            )

    mapping = course_repo.map_topic_to_course(
        db,
        course_id,
        topic_id,
        sequence_order
    )

    return mapping


def get_topics_by_course_service(db: Session, course_id: int):

    mappings = course_repo.get_topics_by_course(
        db,
        course_id
    )

    return mappings


def get_university_by_course_service(db: Session, course_id: int):
    # Validate course existence
    course = course_repo.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    university = course_repo.get_university_by_course(db, course_id)

    if not university:
        raise HTTPException(
            status_code=404,
            detail="University not found for this course"
        )

    return university