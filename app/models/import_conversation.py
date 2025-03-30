"""
Pydantic schemas for conversation import in Mirza Mirror.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ImportRequest(BaseModel):
    """Schema for import request."""
    source: str = Field(..., description="Source of the conversation (chatgpt, claude, gemini)")
    format: str = Field(..., description="Format of the conversation (markdown, json)")

class ImportResponse(BaseModel):
    """Schema for import response."""
    conversation_id: str = Field(..., description="ID of the imported conversation")
    source: str = Field(..., description="Source of the conversation")
    format: str = Field(..., description="Format of the conversation")
    message_count: int = Field(..., description="Number of messages in the conversation")
    thoughts: List[str] = Field(..., description="List of thought IDs created from the conversation")

class ThoughtInConversation(BaseModel):
    """Schema for a thought in a conversation."""
    id: str = Field(..., description="Thought ID")
    content: str = Field(..., description="Thought content")
    role: str = Field(..., description="Role (user, assistant)")
    segment_index: float = Field(..., description="Segment index in the conversation")
    created_at: datetime = Field(..., description="Creation timestamp")

class ConversationResponse(BaseModel):
    """Schema for conversation response."""
    id: str = Field(..., description="Conversation ID")
    source: str = Field(..., description="Source of the conversation")
    format: str = Field(..., description="Format of the conversation")
    imported_at: datetime = Field(..., description="Import timestamp")
    original_file: str = Field(..., description="Original file path")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    thoughts: List[ThoughtInConversation] = Field(..., description="Thoughts in the conversation")

class ConversationListResponse(BaseModel):
    """Schema for conversation list response."""
    conversations: List[Any] = Field(..., description="List of conversations")
    
    class Config:
        orm_mode = True
