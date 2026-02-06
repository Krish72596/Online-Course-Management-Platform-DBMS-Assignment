from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


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

    university_id = Column(Integer, ForeignKey("university.university_id"))

    university = relationship("University", back_populates="courses")