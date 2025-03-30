"""
Pydantic schemas for memory-related data in Mirza Mirror.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class MemoryBase(BaseModel):
    """Base schema for memory data."""
    content: str = Field(..., description="Content of the memory")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata for the memory")

class MemoryCreate(MemoryBase):
    """Schema for creating a new memory."""
    user_id: Optional[str] = Field(default=None, description="User ID for the memory")

class MemoryResponse(BaseModel):
    """Schema for memory response."""
    id: str = Field(..., description="Unique identifier for the memory")
    user_id: str = Field(..., description="User ID for the memory")
    thought_id: Optional[str] = Field(default=None, description="Associated thought ID")
    memory: str = Field(..., description="Content of the memory")
    created_at: datetime = Field(..., description="Creation timestamp")
    memory_type: str = Field(..., description="Type of memory (user, session, agent)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    
    class Config:
        orm_mode = True

class MemorySearch(BaseModel):
    """Schema for memory search request."""
    query: str = Field(..., description="Search query")
    user_id: Optional[str] = Field(default=None, description="User ID for the search context")
    limit: int = Field(default=5, description="Maximum number of results to return")

class MemoryResult(BaseModel):
    """Schema for a single memory search result."""
    id: str = Field(..., description="Memory ID")
    memory: str = Field(..., description="Memory content")
    score: float = Field(..., description="Relevance score")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Memory metadata")

class MemorySearchResponse(BaseModel):
    """Schema for memory search response."""
    results: List[Dict[str, Any]] = Field(..., description="Search results")

class ReflectionResponse(BaseModel):
    """Schema for reflection response."""
    reflection: str = Field(..., description="Generated reflection")
    based_on: List[Dict[str, Any]] = Field(..., description="Memories used for reflection")
