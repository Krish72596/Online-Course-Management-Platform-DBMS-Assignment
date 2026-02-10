from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.teaching import Teaching
from app.models.student import Student
from app.models.instructor import Instructor
from app.models.user import User
from app.models.statistics import Statistics
from app.models.student_statistics import StudentStatistics
from app.models.instructor_statistics import InstructorStatistics


# ============================================================
# PLATFORM OVERVIEW
# ============================================================

def get_platform_overview_service(db: Session):
    """Get overall platform statistics"""
    
    # Total counts
    total_courses = db.query(func.count(Course.course_id)).scalar() or 0
    total_students = db.query(func.count(Student.user_id)).scalar() or 0
    total_instructors = db.query(func.count(Instructor.user_id)).scalar() or 0
    total_enrollments = db.query(func.count(Enrollment.student_user_id)).scalar() or 0
    
    # Completion stats
    completed_enrollments = db.query(func.count(Enrollment.student_user_id)).filter(
        Enrollment.completion_status == "Completed"
    ).scalar() or 0
    
    active_enrollments = total_enrollments - completed_enrollments
    
    # Overall completion rate
    completion_rate = 0
    if total_enrollments > 0:
        completion_rate = round((completed_enrollments / total_enrollments) * 100, 2)
    
    # Get average course enrollments
    avg_enrollments = 0
    if total_courses > 0:
        avg_enrollments = round(total_enrollments / total_courses, 2)
    
    return {
        "total_courses": total_courses,
        "total_students": total_students,
        "total_instructors": total_instructors,
        "total_enrollments": total_enrollments,
        "completed_enrollments": completed_enrollments,
        "active_enrollments": active_enrollments,
        "overall_completion_rate": completion_rate,
        "average_enrollments_per_course": avg_enrollments
    }


# ============================================================
# COURSES ANALYTICS
# ============================================================

def get_all_courses_analytics_service(db: Session):
    """Get analytics for all courses"""
    
    courses = db.query(Course).all()
    
    if not courses:
        return {"courses": []}
    
    courses_data = []
    
    for course in courses:
        # Count enrollments
        total_enrollments = db.query(func.count(Enrollment.student_user_id)).filter(
            Enrollment.course_id == course.course_id
        ).scalar() or 0
        
        completed = db.query(func.count(Enrollment.student_user_id)).filter(
            Enrollment.course_id == course.course_id,
            Enrollment.completion_status == "Completed"
        ).scalar() or 0
        
        active = total_enrollments - completed
        
        # Completion rate
        completion_rate = 0
        if total_enrollments > 0:
            completion_rate = round((completed / total_enrollments) * 100, 2)
        
        # Get average rating
        avg_rating = db.query(func.avg(Enrollment.rating)).filter(
            Enrollment.course_id == course.course_id,
            Enrollment.rating.isnot(None)
        ).scalar()
        
        avg_rating = round(float(avg_rating), 2) if avg_rating else 0
        
        # Get instructors
        instructors = db.query(Teaching).filter(
            Teaching.course_id == course.course_id
        ).count()
        
        courses_data.append({
            "course_id": course.course_id,
            "title": course.title,
            "category": course.category,
            "level": course.level,
            "description": course.description,
            "total_enrollments": total_enrollments,
            "completed_enrollments": completed,
            "active_enrollments": active,
            "completion_rate": completion_rate,
            "average_rating": avg_rating,
            "total_instructors": instructors
        })
    
    # Sort by total enrollments descending
    courses_data.sort(key=lambda x: x["total_enrollments"], reverse=True)
    
    return {
        "total_courses": len(courses_data),
        "courses": courses_data
    }


def get_course_detailed_analytics_service(db: Session, course_id: int):
    """Get detailed analytics for a specific course including enrolled students"""
    
    course = db.query(Course).filter(Course.course_id == course_id).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Get enrollments with student details
    enrollments = db.query(
        Enrollment,
        User
    ).join(
        User,
        User.user_id == Enrollment.student_user_id
    ).filter(
        Enrollment.course_id == course_id
    ).all()
    
    students_data = []
    total_enrollments = 0
    completed_count = 0
    
    for enrollment, user in enrollments:
        total_enrollments += 1
        if enrollment.completion_status == "Completed":
            completed_count += 1
        
        students_data.append({
            "student_user_id": user.user_id,
            "student_name": user.name,
            "student_email": user.email,
            "enrollment_date": enrollment.enrollment_date.isoformat() if enrollment.enrollment_date else None,
            "completion_status": enrollment.completion_status,
            "completion_date": enrollment.completion_date.isoformat() if enrollment.completion_date else None,
            "rating": enrollment.rating,
            "review_text": enrollment.review_text,
            "grade": enrollment.grade,
            "progress": f"{enrollment.current_topic or 0}"
        })
    
    # Get instructors
    instructors = db.query(Teaching, User).join(
        User,
        User.user_id == Teaching.instructor_user_id
    ).filter(
        Teaching.course_id == course_id
    ).all()
    
    instructors_data = []
    for teaching, user in instructors:
        instructors_data.append({
            "instructor_user_id": user.user_id,
            "instructor_name": user.name,
            "instructor_email": user.email,
            "role_in_course": teaching.role_in_course,
            "assigned_date": teaching.assigned_date.isoformat() if teaching.assigned_date else None
        })
    
    completion_rate = 0
    if total_enrollments > 0:
        completion_rate = round((completed_count / total_enrollments) * 100, 2)
    
    return {
        "course_id": course.course_id,
        "title": course.title,
        "category": course.category,
        "level": course.level,
        "description": course.description,
        "duration": course.duration,
        "total_enrollments": total_enrollments,
        "completed_enrollments": completed_count,
        "active_enrollments": total_enrollments - completed_count,
        "completion_rate": completion_rate,
        "instructors": instructors_data,
        "students": students_data
    }


# ============================================================
# STUDENTS ANALYTICS
# ============================================================

def get_all_students_analytics_service(db: Session):
    """Get analytics for all students on the platform"""
    
    students = db.query(User).filter(User.role == "Student").all()
    
    if not students:
        return {"students": []}
    
    students_data = []
    
    for student in students:
        # Get enrollment stats
        total_enrollments = db.query(func.count(Enrollment.course_id)).filter(
            Enrollment.student_user_id == student.user_id
        ).scalar() or 0
        
        completed = db.query(func.count(Enrollment.course_id)).filter(
            Enrollment.student_user_id == student.user_id,
            Enrollment.completion_status == "Completed"
        ).scalar() or 0
        
        active = total_enrollments - completed
        
        # Get average rating given
        avg_rating = db.query(func.avg(Enrollment.rating)).filter(
            Enrollment.student_user_id == student.user_id,
            Enrollment.rating.isnot(None)
        ).scalar()
        
        avg_rating = round(float(avg_rating), 2) if avg_rating else 0
        
        # Get statistics from StudentStatistics table
        stats = db.query(StudentStatistics).filter(
            StudentStatistics.student_user_id == student.user_id
        ).first()
        
        last_updated = None
        if stats:
            last_updated = stats.last_updated.isoformat() if stats.last_updated else None
        
        students_data.append({
            "student_user_id": student.user_id,
            "name": student.name,
            "email": student.email,
            "total_enrollments": total_enrollments,
            "completed_courses": completed,
            "active_courses": active,
            "average_rating": avg_rating,
            "last_stats_update": last_updated
        })
    
    # Sort by total enrollments descending
    students_data.sort(key=lambda x: x["total_enrollments"], reverse=True)
    
    return {
        "total_students": len(students_data),
        "students": students_data
    }


# ============================================================
# INSTRUCTORS ANALYTICS
# ============================================================

def get_all_instructors_analytics_service(db: Session):
    """Get analytics for all instructors on the platform"""
    
    instructors = db.query(User).filter(User.role == "Instructor").all()
    
    if not instructors:
        return {"instructors": []}
    
    instructors_data = []
    
    for instructor in instructors:
        # Get teaching stats
        total_courses = db.query(func.count(Teaching.course_id)).filter(
            Teaching.instructor_user_id == instructor.user_id
        ).scalar() or 0
        
        # Get total students across all courses taught
        total_students = db.query(func.count(Enrollment.student_user_id)).join(
            Teaching,
            Teaching.course_id == Enrollment.course_id
        ).filter(
            Teaching.instructor_user_id == instructor.user_id
        ).scalar() or 0
        
        # Get average course completion for courses taught
        courses = db.query(Teaching.course_id).filter(
            Teaching.instructor_user_id == instructor.user_id
        ).all()
        
        avg_completion_rate = 0
        if courses:
            completion_rates = []
            for (course_id,) in courses:
                enrollments = db.query(func.count(Enrollment.student_user_id)).filter(
                    Enrollment.course_id == course_id
                ).scalar() or 0
                
                completed = db.query(func.count(Enrollment.student_user_id)).filter(
                    Enrollment.course_id == course_id,
                    Enrollment.completion_status == "Completed"
                ).scalar() or 0
                
                if enrollments > 0:
                    rate = (completed / enrollments) * 100
                    completion_rates.append(rate)
            
            if completion_rates:
                avg_completion_rate = round(sum(completion_rates) / len(completion_rates), 2)
        
        # Get statistics from InstructorStatistics table
        stats = db.query(InstructorStatistics).filter(
            InstructorStatistics.instructor_user_id == instructor.user_id
        ).first()
        
        last_updated = None
        if stats:
            last_updated = stats.last_updated.isoformat() if stats.last_updated else None
        
        instructors_data.append({
            "instructor_user_id": instructor.user_id,
            "name": instructor.name,
            "email": instructor.email,
            "total_courses_taught": total_courses,
            "total_students": total_students,
            "average_course_completion_rate": avg_completion_rate,
            "last_stats_update": last_updated
        })
    
    # Sort by total courses taught descending
    instructors_data.sort(key=lambda x: x["total_courses_taught"], reverse=True)
    
    return {
        "total_instructors": len(instructors_data),
        "instructors": instructors_data
    }
