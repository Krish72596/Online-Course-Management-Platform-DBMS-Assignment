from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class InstructorStatistics(Base):
    __tablename__ = "instructor_statistics"

    instructor_user_id = Column(Integer, ForeignKey("instructor.user_id", ondelete="CASCADE"), primary_key=True)

    total_courses_taught = Column(Integer, default=0)
    total_students = Column(Integer, default=0)

    last_updated = Column(TIMESTAMP, server_default=func.now())