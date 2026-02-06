from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class CourseTopic(Base):
    __tablename__ = "course_topic"

    course_id = Column(Integer, ForeignKey("course.course_id", ondelete="CASCADE"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topic.topic_id", ondelete="CASCADE"), primary_key=True)

    sequence_order = Column(Integer)