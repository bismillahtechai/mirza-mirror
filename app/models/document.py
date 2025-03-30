"""
Script to create a document model file for Mirza Mirror.
"""

from sqlalchemy import Column, String, Text, DateTime, JSONB
from datetime import datetime
import uuid

from app.db.database import Base

class Document(Base):
    """Document model."""
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    file_path = Column(String, nullable=False)
    content = Column(Text)
    content_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    docling_representation = Column(JSONB)
    metadata = Column(JSONB)
