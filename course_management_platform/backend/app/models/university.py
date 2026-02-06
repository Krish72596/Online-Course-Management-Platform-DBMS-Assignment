from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class University(Base):
    __tablename__ = "university"

    university_id = Column(Integer, primary_key=True)

    name = Column(String(150), nullable=False)
    region = Column(String(100))
    country = Column(String(50))
    website = Column(String(200))

    courses = relationship("Course", back_populates="university")