from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Course(Base):
    __tablename__ = "course"

    course_id = Column(Integer, primary_key=True)

    title = Column(String(150), nullable=False)
    description = Column(Text)
    category = Column(String(50))
    level = Column(String(50))
    language = Column(String(50))
    start_date = Column(Date)
    duration = Column(Integer)
    quiz_answer_key = Column(Text, nullable=True)  # Flexible length answer key (one char per question)

    university_id = Column(Integer, ForeignKey("university.university_id"))
    
    # Approval workflow fields
    created_by = Column(Integer, ForeignKey("instructor.user_id", ondelete="SET NULL"), nullable=True)
    approval_status = Column(String(20), default='Pending')
    approved_by = Column(Integer, ForeignKey("administrator.user_id", ondelete="SET NULL"), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    university = relationship("University", back_populates="courses")
    instructor = relationship("Instructor", foreign_keys=[created_by])