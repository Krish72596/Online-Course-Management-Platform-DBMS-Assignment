from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20))
    role = Column(String(30), nullable=False)

    last_login = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # ISA relationships
    student = relationship("Student", back_populates="user", uselist=False)
    instructor = relationship("Instructor", back_populates="user", uselist=False)
    administrator = relationship("Administrator", back_populates="user", uselist=False)
    analyst = relationship("DataAnalyst", back_populates="user", uselist=False)