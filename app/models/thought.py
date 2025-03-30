"""
Models module for Mirza Mirror.
This module contains SQLAlchemy models for the database.
"""

from sqlalchemy import Column, String, Text, Float, Boolean, Integer, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.db.database import Base

# Association table for thought tags
thought_tags = Table(
    'thought_tags',
    Base.metadata,
    Column('thought_id', String, ForeignKey('thoughts.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', String, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

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

class Thought(Base):
    """Thought model."""
    __tablename__ = "thoughts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    source = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    audio_file = Column(String)
    document_file = Column(String)
    summary = Column(Text)
    metadata = Column(JSONB)
    user_id = Column(String, ForeignKey('users.id'))

    # Relationships
    user = relationship("User", back_populates="thoughts")
    tags = relationship("Tag", secondary=thought_tags, back_populates="thoughts")
    source_links = relationship("Link", foreign_keys="Link.source_thought_id", back_populates="source_thought")
    target_links = relationship("Link", foreign_keys="Link.target_thought_id", back_populates="target_thought")
    conversation_thoughts = relationship("ConversationThought", back_populates="thought")
    actions = relationship("Action", back_populates="thought")

class Tag(Base):
    """Tag model."""
    __tablename__ = "tags"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)  # 'auto', 'custom', etc.
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    thoughts = relationship("Thought", secondary=thought_tags, back_populates="tags")

class Link(Base):
    """Link model for connecting related thoughts."""
    __tablename__ = "links"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_thought_id = Column(String, ForeignKey('thoughts.id', ondelete='CASCADE'), nullable=False)
    target_thought_id = Column(String, ForeignKey('thoughts.id', ondelete='CASCADE'), nullable=False)
    relationship = Column(String, nullable=False)  # 'similar', 'continuation', 'contradiction', 'inspiration'
    strength = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    source_thought = relationship("Thought", foreign_keys=[source_thought_id], back_populates="source_links")
    target_thought = relationship("Thought", foreign_keys=[target_thought_id], back_populates="target_links")

class ImportedConversation(Base):
    """Imported conversation model."""
    __tablename__ = "imported_conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String, nullable=False)  # 'chatgpt', 'claude', 'gemini'
    format = Column(String, nullable=False)  # 'markdown', 'json'
    original_file = Column(String, nullable=False)
    imported_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    metadata = Column(JSONB)

    # Relationships
    conversation_thoughts = relationship("ConversationThought", back_populates="conversation")

class ConversationThought(Base):
    """Association model for conversations and thoughts."""
    __tablename__ = "conversation_thoughts"

    conversation_id = Column(String, ForeignKey('imported_conversations.id', ondelete='CASCADE'), primary_key=True)
    thought_id = Column(String, ForeignKey('thoughts.id', ondelete='CASCADE'), primary_key=True)
    segment_index = Column(Integer, nullable=False)
    role = Column(String, nullable=False)  # 'user', 'assistant'

    # Relationships
    conversation = relationship("ImportedConversation", back_populates="conversation_thoughts")
    thought = relationship("Thought", back_populates="conversation_thoughts")

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

class Action(Base):
    """Action model for tasks extracted from thoughts."""
    __tablename__ = "actions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    thought_id = Column(String, ForeignKey('thoughts.id', ondelete='CASCADE'), nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(String, nullable=False)  # 'high', 'medium', 'low'
    due_date = Column(String)
    completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    thought = relationship("Thought", back_populates="actions")
