from sqlalchemy import Column, Integer, Date, String, ForeignKey
from app.database import Base


class Teaching(Base):
    __tablename__ = "teaching"

    course_id = Column(Integer, ForeignKey("course.course_id", ondelete="CASCADE"), primary_key=True)
    instructor_user_id = Column(Integer, ForeignKey("instructor.user_id", ondelete="CASCADE"), primary_key=True)

    assigned_date = Column(Date)
    role_in_course = Column(String(50))