from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class StudentStatistics(Base):
    __tablename__ = "student_statistics"

    student_user_id = Column(Integer, ForeignKey("student.user_id", ondelete="CASCADE"), primary_key=True)

    total_enrollments = Column(Integer, default=0)
    completed_courses = Column(Integer, default=0)
    active_courses = Column(Integer, default=0)

    last_updated = Column(TIMESTAMP, server_default=func.now())