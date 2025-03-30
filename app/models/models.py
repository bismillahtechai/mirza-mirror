"""
Database models for Mirza Mirror application.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Table, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association table for thought-tag many-to-many relationship
thought_tag = Table(
    'thought_tag',
    Base.metadata,
    Column('thought_id', String, ForeignKey('thoughts.id')),
    Column('tag_id', String, ForeignKey('tags.id')),
    Column('confidence', Float),
    Column('created_at', DateTime, default=datetime.utcnow)
)

# Association table for reflection-thought many-to-many relationship
reflection_thought = Table(
    'reflection_thought',
    Base.metadata,
    Column('reflection_id', String, ForeignKey('reflections.id')),
    Column('thought_id', String, ForeignKey('thoughts.id')),
    Column('created_at', DateTime, default=datetime.utcnow)
)

class Thought(Base):
    """Thought model representing a captured thought."""
    
    __tablename__ = 'thoughts'
    
    id = Column(String, primary_key=True)
    content = Column(Text, nullable=False)
    source = Column(String, nullable=False)  # voice_note, text_note, document, import
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    audio_file = Column(String, nullable=True)
    document_file = Column(String, nullable=True)
    embedding_id = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    tags = relationship("Tag", secondary=thought_tag, back_populates="thoughts")
    actions = relationship("Action", back_populates="thought")
    links_as_source = relationship("Link", foreign_keys="Link.source_thought_id", back_populates="source_thought")
    links_as_target = relationship("Link", foreign_keys="Link.target_thought_id", back_populates="target_thought")
    reflections = relationship("Reflection", secondary=reflection_thought, back_populates="related_thoughts")
    documents = relationship("Document", back_populates="thought")
    memories = relationship("Memory", back_populates="thought")

class Memory(Base):
    """Memory model representing a memory stored in mem0."""
    
    __tablename__ = 'memories'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    thought_id = Column(String, ForeignKey('thoughts.id'), nullable=True)
    memory = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    relevance_score = Column(Float, nullable=True)
    memory_type = Column(String, nullable=False)  # user, session, agent
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    thought = relationship("Thought", back_populates="memories")

class Document(Base):
    """Document model representing a document processed by Docling."""
    
    __tablename__ = 'documents'
    
    id = Column(String, primary_key=True)
    thought_id = Column(String, ForeignKey('thoughts.id'), nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    docling_representation = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    thought = relationship("Thought", back_populates="documents")

class ImportedConversation(Base):
    """ImportedConversation model representing an imported conversation from an AI assistant."""
    
    __tablename__ = 'imported_conversations'
    
    id = Column(String, primary_key=True)
    source = Column(String, nullable=False)  # chatgpt, claude, gemini
    format = Column(String, nullable=False)  # markdown, json
    original_file = Column(String, nullable=False)
    imported_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    conversation_thoughts = relationship("ConversationThought", back_populates="conversation")

class ConversationThought(Base):
    """ConversationThought model linking imported conversations to thoughts."""
    
    __tablename__ = 'conversation_thoughts'
    
    conversation_id = Column(String, ForeignKey('imported_conversations.id'), primary_key=True)
    thought_id = Column(String, ForeignKey('thoughts.id'), primary_key=True)
    segment_index = Column(Float, nullable=False)
    role = Column(String, nullable=False)  # user, assistant
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("ImportedConversation", back_populates="conversation_thoughts")
    thought = relationship("Thought")

class Tag(Base):
    """Tag model representing a category, project, emotion, or other classification."""
    
    __tablename__ = 'tags'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # project, emotion, category, custom
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    thoughts = relationship("Thought", secondary=thought_tag, back_populates="tags")

class Link(Base):
    """Link model representing a connection between two thoughts."""
    
    __tablename__ = 'links'
    
    id = Column(String, primary_key=True)
    source_thought_id = Column(String, ForeignKey('thoughts.id'), nullable=False)
    target_thought_id = Column(String, ForeignKey('thoughts.id'), nullable=False)
    relationship = Column(String, nullable=False)  # similar, continuation, contradiction, inspiration
    strength = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    source_thought = relationship("Thought", foreign_keys=[source_thought_id], back_populates="links_as_source")
    target_thought = relationship("Thought", foreign_keys=[target_thought_id], back_populates="links_as_target")

class Action(Base):
    """Action model representing a task or action item extracted from a thought."""
    
    __tablename__ = 'actions'
    
    id = Column(String, primary_key=True)
    thought_id = Column(String, ForeignKey('thoughts.id'), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String, nullable=False)  # pending, completed, dismissed
    due_date = Column(DateTime, nullable=True)
    priority = Column(String, nullable=False)  # high, medium, low
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    thought = relationship("Thought", back_populates="actions")

class Reflection(Base):
    """Reflection model representing an AI-generated insight or pattern."""
    
    __tablename__ = 'reflections'
    
    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)  # insight, pattern, summary
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    related_thoughts = relationship("Thought", secondary=reflection_thought, back_populates="reflections")
