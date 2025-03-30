"""
API routes for memory management in Mirza Mirror.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database import get_db
from app.models import Memory, Thought
from app.services.memory_service import MemoryService
from app.schemas.memory import (
    MemoryCreate, 
    MemoryResponse, 
    MemorySearch, 
    MemorySearchResponse,
    ReflectionResponse
)

router = APIRouter(
    prefix="/api/memory",
    tags=["memory"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
def create_memory(
    memory_data: MemoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new memory from content.
    """
    # Initialize memory service
    memory_service = MemoryService(user_id=memory_data.user_id)
    
    # Create a temporary thought to associate with the memory
    thought = Thought(
        id=str(uuid4()),
        content=memory_data.content,
        source="api",
        metadata=memory_data.metadata
    )
    
    # Create memory
    db_memory = memory_service.create_memory_from_thought(db, thought)
    
    return db_memory

@router.post("/search", response_model=MemorySearchResponse)
def search_memories(
    search_data: MemorySearch,
    db: Session = Depends(get_db)
):
    """
    Search for memories based on a query.
    """
    # Initialize memory service
    memory_service = MemoryService(user_id=search_data.user_id)
    
    # Search for memories
    memories = memory_service.search_memories(
        query=search_data.query,
        limit=search_data.limit
    )
    
    return {"results": memories}

@router.get("/thought/{thought_id}", response_model=MemorySearchResponse)
def get_memories_for_thought(
    thought_id: str,
    limit: int = 5,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get memories related to a specific thought.
    """
    # Initialize memory service
    memory_service = MemoryService(user_id=user_id)
    
    # Get memories for thought
    memories = memory_service.get_memories_for_thought(
        db=db,
        thought_id=thought_id,
        limit=limit
    )
    
    return {"results": memories}

@router.post("/reflection", response_model=ReflectionResponse)
def generate_reflection(
    context: str,
    limit: int = 5,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Generate a reflection based on memories.
    """
    # Initialize memory service
    memory_service = MemoryService(user_id=user_id)
    
    # Generate reflection
    reflection = memory_service.generate_reflection(
        context=context,
        limit=limit
    )
    
    return reflection

@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memory(
    memory_id: str,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Delete a memory.
    """
    # Initialize memory service
    memory_service = MemoryService(user_id=user_id)
    
    # Delete memory
    success = memory_service.delete_memory(db, memory_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memory with ID {memory_id} not found"
        )
