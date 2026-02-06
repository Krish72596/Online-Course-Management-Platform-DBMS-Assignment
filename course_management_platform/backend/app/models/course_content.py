from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from app.database import Base


class CourseContent(Base):
    __tablename__ = "course_content"

    content_id = Column(Integer, primary_key=True)

    title = Column(String(150), nullable=False)
    content_type = Column(String(50))
    upload_date = Column(Date)
    file_url = Column(Text, nullable=False)

    course_id = Column(Integer, ForeignKey("course.course_id", ondelete="CASCADE"))
    topic_id = Column(Integer, ForeignKey("topic.topic_id", ondelete="SET NULL"))
    instructor_user_id = Column(Integer, ForeignKey("instructor.user_id", ondelete="SET NULL"))