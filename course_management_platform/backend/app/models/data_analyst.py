from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class DataAnalyst(Base):
    __tablename__ = "data_analyst"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    qualification = Column(String(100))
    assigned_since = Column(Date)

    user = relationship("User", back_populates="analyst")