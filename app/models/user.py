"""
Script to create a user model file for Mirza Mirror.
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base

class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    thoughts = relationship("Thought", back_populates="user")
