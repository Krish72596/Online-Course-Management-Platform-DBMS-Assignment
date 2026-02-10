from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.analyst_service import (
    get_platform_overview_service,
    get_all_courses_analytics_service,
    get_all_students_analytics_service,
    get_all_instructors_analytics_service,
    get_course_detailed_analytics_service
)

# Router Config
router = APIRouter(
    prefix="/analyst",
    tags=["Data Analyst Dashboard"]
)

# PLATFORM OVERVIEW
@router.get("/overview")
def get_platform_overview(db: Session = Depends(get_db)):
    """Get platform-wide overview statistics"""
    return get_platform_overview_service(db)


# COURSES ANALYTICS
@router.get("/courses/analytics")
def get_courses_analytics(db: Session = Depends(get_db)):
    """Get analytics for all courses"""
    return get_all_courses_analytics_service(db)


@router.get("/courses/{course_id}/detailed")
def get_course_detailed_analytics(course_id: int, db: Session = Depends(get_db)):
    """Get detailed analytics for a specific course including enrolled students"""
    return get_course_detailed_analytics_service(db, course_id)


# STUDENTS ANALYTICS
@router.get("/students/analytics")
def get_students_analytics(db: Session = Depends(get_db)):
    """Get analytics for all students on the platform"""
    return get_all_students_analytics_service(db)


# INSTRUCTORS ANALYTICS
@router.get("/instructors/analytics")
def get_instructors_analytics(db: Session = Depends(get_db)):
    """Get analytics for all instructors on the platform"""
    return get_all_instructors_analytics_service(db)
