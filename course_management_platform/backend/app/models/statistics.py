from sqlalchemy import Column, Integer, Numeric, ForeignKey
from app.database import Base


class Statistics(Base):
    __tablename__ = "statistics"

    course_id = Column(Integer, ForeignKey("course.course_id", ondelete="CASCADE"), primary_key=True)

    total_enrollments = Column(Integer)
    active_enrollments = Column(Integer)
    completion_rate = Column(Numeric(5, 2))
    average_completion_time = Column(Integer)