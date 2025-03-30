"""
API routes for thought capture in Mirza Mirror.
"""

import os
import shutil
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database import get_db
from app.capture import CaptureProcessor
from app.schemas.capture import (
    TextThoughtRequest,
    ThoughtResponse,
    TagsRequest,
    TagsResponse,
    SearchRequest,
    SearchResponse,
    ThoughtListResponse
)

router = APIRouter(
    prefix="/api/thoughts",
    tags=["thoughts"],
    responses={404: {"description": "Not found"}},
)

@router.post("/text", response_model=ThoughtResponse, status_code=status.HTTP_201_CREATED)
async def create_text_thought(
    thought_data: TextThoughtRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new text thought.
    
    Args:
        thought_data: Text thought data
        db: Database session
    """
    processor = CaptureProcessor()
    result = processor.process_text_thought(db, thought_data.content, thought_data.user_id)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.post("/audio", response_model=ThoughtResponse, status_code=status.HTTP_201_CREATED)
async def create_audio_thought(
    file: UploadFile = File(...),
    transcription: str = Form(...),
    user_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Create a new audio thought.
    
    Args:
        file: Audio file
        transcription: Transcription of the audio
        user_id: User ID
        db: Database session
    """
    processor = CaptureProcessor()
    
    # Save the audio file
    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(processor.audio_dir, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving audio file: {str(e)}"
        )
    
    # Process the audio thought
    result = processor.process_audio_thought(db, file_path, transcription, user_id)
    
    if "error" in result:
        # Clean up the file if processing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.post("/{thought_id}/tags", response_model=TagsResponse)
async def add_tags_to_thought(
    thought_id: str,
    tags_data: TagsRequest,
    db: Session = Depends(get_db)
):
    """
    Add tags to a thought.
    
    Args:
        thought_id: Thought ID
        tags_data: Tags data
        db: Database session
    """
    processor = CaptureProcessor()
    result = processor.add_tags_to_thought(db, thought_id, tags_data.tags)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in result["error"] else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.post("/search", response_model=SearchResponse)
async def search_thoughts(
    search_data: SearchRequest,
    db: Session = Depends(get_db)
):
    """
    Search for thoughts.
    
    Args:
        search_data: Search data
        db: Database session
    """
    processor = CaptureProcessor()
    result = processor.search_thoughts(db, search_data.query, search_data.limit, search_data.user_id)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.get("/{thought_id}", response_model=ThoughtResponse)
async def get_thought(
    thought_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a thought by ID.
    
    Args:
        thought_id: Thought ID
        db: Database session
    """
    processor = CaptureProcessor()
    result = processor.get_thought_by_id(db, thought_id)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in result["error"] else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.get("/", response_model=ThoughtListResponse)
async def get_recent_thoughts(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get recent thoughts.
    
    Args:
        limit: Maximum number of results
        db: Database session
    """
    processor = CaptureProcessor()
    result = processor.get_recent_thoughts(db, limit)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.get("/tag/{tag_name}", response_model=ThoughtListResponse)
async def get_thoughts_by_tag(
    tag_name: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get thoughts by tag.
    
    Args:
        tag_name: Tag name
        limit: Maximum number of results
        db: Database session
    """
    processor = CaptureProcessor()
    result = processor.get_thoughts_by_tag(db, tag_name, limit)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in result["error"] else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.delete("/{thought_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thought(
    thought_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a thought.
    
    Args:
        thought_id: Thought ID
        db: Database session
    """
    processor = CaptureProcessor()
    result = processor.delete_thought(db, thought_id)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in result["error"] else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
