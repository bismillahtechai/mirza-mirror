"""
API routes for agent services in Mirza Mirror.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.agents import AgentManager
from app.schemas.agents import (
    TaggingRequest,
    TaggingResponse,
    LinkingRequest,
    LinkingResponse,
    ReflectionRequest,
    ReflectionResponse,
    ActionRequest,
    ActionResponse,
    ProcessThoughtRequest,
    ProcessThoughtResponse
)

router = APIRouter(
    prefix="/api/agents",
    tags=["agents"],
    responses={404: {"description": "Not found"}},
)

@router.post("/process", response_model=ProcessThoughtResponse)
async def process_thought(
    request: ProcessThoughtRequest,
    db: Session = Depends(get_db)
):
    """
    Process a thought using all agents.
    
    Args:
        request: Process thought request
        db: Database session
    """
    agent_manager = AgentManager()
    
    # Get existing thoughts if needed
    existing_thoughts = []
    if request.include_existing_thoughts:
        from app.models import Thought
        existing_thoughts_query = db.query(Thought)
        
        # Limit to recent thoughts
        existing_thoughts_query = existing_thoughts_query.order_by(Thought.created_at.desc()).limit(10)
        
        # Convert to list of dicts
        existing_thoughts = [
            {
                "id": thought.id,
                "content": thought.content,
                "source": thought.source,
                "created_at": thought.created_at
            }
            for thought in existing_thoughts_query.all()
        ]
    
    # Process the thought
    result = agent_manager.process_thought(request.content, existing_thoughts)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.post("/tags", response_model=TaggingResponse)
async def generate_tags(
    request: TaggingRequest,
    db: Session = Depends(get_db)
):
    """
    Generate tags for a thought.
    
    Args:
        request: Tagging request
        db: Database session
    """
    agent_manager = AgentManager()
    result = agent_manager.generate_tags(request.content)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.post("/links", response_model=LinkingResponse)
async def find_related_thoughts(
    request: LinkingRequest,
    db: Session = Depends(get_db)
):
    """
    Find thoughts related to the given thought.
    
    Args:
        request: Linking request
        db: Database session
    """
    agent_manager = AgentManager()
    
    # Get existing thoughts
    from app.models import Thought
    existing_thoughts_query = db.query(Thought)
    
    # Apply filters if provided
    if request.filter_by_tag:
        existing_thoughts_query = existing_thoughts_query.join(Thought.tags).filter(
            Thought.tags.any(name=request.filter_by_tag)
        )
    
    # Limit to recent thoughts
    existing_thoughts_query = existing_thoughts_query.order_by(Thought.created_at.desc()).limit(request.max_thoughts)
    
    # Convert to list of dicts
    existing_thoughts = [
        {
            "id": thought.id,
            "content": thought.content,
            "source": thought.source,
            "created_at": thought.created_at
        }
        for thought in existing_thoughts_query.all()
    ]
    
    # Find related thoughts
    result = agent_manager.find_related_thoughts(request.content, existing_thoughts)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.post("/reflection", response_model=ReflectionResponse)
async def generate_reflection(
    request: ReflectionRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a reflection based on thought content.
    
    Args:
        request: Reflection request
        db: Database session
    """
    agent_manager = AgentManager()
    
    # Get related thoughts if thought_id is provided
    related_thoughts = []
    if request.thought_id:
        from app.models import Thought, Link
        
        # Get the thought
        thought = db.query(Thought).filter(Thought.id == request.thought_id).first()
        if not thought:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Thought with ID {request.thought_id} not found"
            )
        
        # Get related thoughts
        related_thought_ids = []
        
        # Get thoughts linked as source
        source_links = db.query(Link).filter(Link.source_thought_id == request.thought_id).all()
        related_thought_ids.extend([link.target_thought_id for link in source_links])
        
        # Get thoughts linked as target
        target_links = db.query(Link).filter(Link.target_thought_id == request.thought_id).all()
        related_thought_ids.extend([link.source_thought_id for link in target_links])
        
        # Get related thoughts
        if related_thought_ids:
            related_thoughts_query = db.query(Thought).filter(Thought.id.in_(related_thought_ids))
            related_thoughts = [
                {
                    "id": thought.id,
                    "content": thought.content,
                    "source": thought.source,
                    "created_at": thought.created_at
                }
                for thought in related_thoughts_query.all()
            ]
    
    # Generate reflection
    result = agent_manager.generate_reflection(request.content, related_thoughts)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.post("/actions", response_model=ActionResponse)
async def extract_actions(
    request: ActionRequest,
    db: Session = Depends(get_db)
):
    """
    Extract actionable items from thought content.
    
    Args:
        request: Action request
        db: Database session
    """
    agent_manager = AgentManager()
    result = agent_manager.extract_actions(request.content)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result
