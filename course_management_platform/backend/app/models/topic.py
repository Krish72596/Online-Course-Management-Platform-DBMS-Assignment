from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Topic(Base):
    __tablename__ = "topic"

    topic_id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)