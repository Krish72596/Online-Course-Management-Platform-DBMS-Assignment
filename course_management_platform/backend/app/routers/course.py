from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course_schema import (
    UniversityCreate,
    UniversityResponse,
    CourseCreate,
    CourseResponse
)
from app.services.course_service import (
    create_university_service,
    get_all_universities_service,
    create_course_service,
    get_all_courses_service,
    get_course_by_id_service
)

# Router Config
router = APIRouter(
    prefix="",
    tags=["Academic - Courses"]
)


# UNIVERSITY ROUTES
@router.post(
    "/universities",
    response_model=UniversityResponse
)
def create_university(
    payload: UniversityCreate,
    db: Session = Depends(get_db)
):
    return create_university_service(db, payload)


@router.get(
    "/universities",
    response_model=list[UniversityResponse]
)
def get_universities(
    db: Session = Depends(get_db)
):
    return get_all_universities_service(db)


# COURSE ROUTES
@router.post(
    "/courses",
    response_model=CourseResponse
)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db)
):
    return create_course_service(db, payload)


@router.get(
    "/courses",
    response_model=list[CourseResponse]
)
def get_courses(
    db: Session = Depends(get_db)
):
    return get_all_courses_service(db)


@router.get(
    "/courses/{course_id}",
    response_model=CourseResponse
)
def get_course_by_id(
    course_id: int,
    db: Session = Depends(get_db)
):
    return get_course_by_id_service(db, course_id)