"""
Pydantic schemas for agent services in Mirza Mirror.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class TaggingRequest(BaseModel):
    """Schema for tagging request."""
    content: str = Field(..., description="Thought content to generate tags for")

class Tag(BaseModel):
    """Schema for a tag."""
    name: str = Field(..., description="Tag name")
    confidence: float = Field(..., description="Confidence score (0-1)")
    type: str = Field(..., description="Tag type (auto, custom)")

class TaggingResponse(BaseModel):
    """Schema for tagging response."""
    tags: List[Dict[str, Any]] = Field(..., description="Generated tags")

class LinkingRequest(BaseModel):
    """Schema for linking request."""
    content: str = Field(..., description="Thought content to find related thoughts for")
    filter_by_tag: Optional[str] = Field(default=None, description="Filter existing thoughts by tag")
    max_thoughts: int = Field(default=10, description="Maximum number of existing thoughts to consider")

class Link(BaseModel):
    """Schema for a link between thoughts."""
    thought_id: str = Field(..., description="Related thought ID")
    relationship: str = Field(..., description="Relationship type (similar, continuation, contradiction, inspiration)")
    strength: float = Field(..., description="Relationship strength (0-1)")

class LinkingResponse(BaseModel):
    """Schema for linking response."""
    links: List[Dict[str, Any]] = Field(..., description="Related thoughts")

class ReflectionRequest(BaseModel):
    """Schema for reflection request."""
    content: str = Field(..., description="Thought content to generate reflection for")
    thought_id: Optional[str] = Field(default=None, description="Thought ID to include related thoughts")

class ReflectionResponse(BaseModel):
    """Schema for reflection response."""
    reflection: str = Field(..., description="Generated reflection")
    summary: Optional[str] = Field(default=None, description="Generated summary")

class ActionRequest(BaseModel):
    """Schema for action request."""
    content: str = Field(..., description="Thought content to extract actions from")

class Action(BaseModel):
    """Schema for an action."""
    content: str = Field(..., description="Action content")
    priority: str = Field(..., description="Priority (high, medium, low)")
    due_date: Optional[str] = Field(default=None, description="Due date")

class ActionResponse(BaseModel):
    """Schema for action response."""
    actions: List[Dict[str, Any]] = Field(..., description="Extracted actions")

class ProcessThoughtRequest(BaseModel):
    """Schema for process thought request."""
    content: str = Field(..., description="Thought content to process")
    include_existing_thoughts: bool = Field(default=True, description="Whether to include existing thoughts for context")

class ProcessThoughtResponse(BaseModel):
    """Schema for process thought response."""
    tags: List[Dict[str, Any]] = Field(..., description="Generated tags")
    links: Optional[List[Dict[str, Any]]] = Field(default=None, description="Related thoughts")
    reflection: str = Field(..., description="Generated reflection")
    summary: str = Field(..., description="Generated summary")
    actions: List[Dict[str, Any]] = Field(..., description="Extracted actions")
