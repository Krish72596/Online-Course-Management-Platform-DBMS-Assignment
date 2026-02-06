from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Instructor(Base):
    __tablename__ = "instructor"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    qualification = Column(String(100))
    experience = Column(Integer)
    expertise_area = Column(String(100))
    bio = Column(Text)

    user = relationship("User", back_populates="instructor")