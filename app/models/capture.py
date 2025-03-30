"""
Pydantic schemas for thought capture in Mirza Mirror.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class TextThoughtRequest(BaseModel):
    """Schema for text thought request."""
    content: str = Field(..., description="Thought content")
    user_id: Optional[str] = Field(default=None, description="User ID")

class ThoughtResponse(BaseModel):
    """Schema for thought response."""
    id: Optional[str] = Field(default=None, alias="thought_id", description="Thought ID")
    content: Optional[str] = Field(default=None, description="Thought content")
    source: Optional[str] = Field(default=None, description="Source of the thought")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Update timestamp")
    audio_file: Optional[str] = Field(default=None, description="Path to audio file")
    document_file: Optional[str] = Field(default=None, description="Path to document file")
    summary: Optional[str] = Field(default=None, description="Thought summary")
    tags: Optional[List[str]] = Field(default=None, description="List of tags")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    memory_id: Optional[str] = Field(default=None, description="Associated memory ID")

class TagsRequest(BaseModel):
    """Schema for tags request."""
    tags: List[str] = Field(..., description="List of tag names")

class TagsResponse(BaseModel):
    """Schema for tags response."""
    thought_id: str = Field(..., description="Thought ID")
    added_tags: List[str] = Field(..., description="List of added tag names")
    all_tags: List[str] = Field(..., description="List of all tag names")

class SearchRequest(BaseModel):
    """Schema for search request."""
    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, description="Maximum number of results")
    user_id: Optional[str] = Field(default=None, description="User ID")

class ThoughtInSearch(BaseModel):
    """Schema for a thought in search results."""
    id: str = Field(..., description="Thought ID")
    content: str = Field(..., description="Thought content")
    source: str = Field(..., description="Source of the thought")
    created_at: datetime = Field(..., description="Creation timestamp")
    tags: List[str] = Field(..., description="List of tags")
    relevance: float = Field(..., description="Relevance score")

class SearchResponse(BaseModel):
    """Schema for search response."""
    query: str = Field(..., description="Search query")
    results: List[Dict[str, Any]] = Field(..., description="Search results")

class ThoughtInList(BaseModel):
    """Schema for a thought in a list."""
    id: str = Field(..., description="Thought ID")
    content: str = Field(..., description="Thought content")
    source: str = Field(..., description="Source of the thought")
    created_at: datetime = Field(..., description="Creation timestamp")
    tags: List[str] = Field(..., description="List of tags")

class ThoughtListResponse(BaseModel):
    """Schema for thought list response."""
    thoughts: List[Dict[str, Any]] = Field(..., description="List of thoughts")
    tag: Optional[str] = Field(default=None, description="Tag name (if filtered by tag)")
