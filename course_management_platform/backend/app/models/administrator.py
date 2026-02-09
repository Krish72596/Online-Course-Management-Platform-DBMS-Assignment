from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Administrator(Base):
    __tablename__ = "administrator"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    admin_level = Column(String(30), nullable=False, default="Junior")
    assigned_since = Column(Date)

    user = relationship("User", back_populates="administrator")