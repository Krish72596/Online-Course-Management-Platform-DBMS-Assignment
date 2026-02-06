from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Student(Base):
    __tablename__ = "student"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    date_of_birth = Column(Date)
    country = Column(String(50))
    gender = Column(String(20))
    education_level = Column(String(50))

    user = relationship("User", back_populates="student")