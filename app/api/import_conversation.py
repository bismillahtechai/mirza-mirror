"""
API routes for conversation import in Mirza Mirror.
"""

import os
import shutil
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database import get_db
from app.import_conversation import ConversationImporter
from app.schemas.import_conversation import (
    ImportResponse,
    ConversationResponse,
    ConversationListResponse
)

router = APIRouter(
    prefix="/api/import",
    tags=["import"],
    responses={404: {"description": "Not found"}},
)

@router.post("/conversation", status_code=status.HTTP_201_CREATED)
async def import_conversation(
    file: UploadFile = File(...),
    source: str = Form(...),
    format: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Import a conversation from an AI assistant.
    
    Args:
        file: The conversation file to import
        source: Source of the conversation (chatgpt, claude, gemini)
        format: Format of the conversation (markdown, json)
        db: Database session
    """
    importer = ConversationImporter()
    
    # Check if source is supported
    if source.lower() not in importer.get_supported_sources():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported source: {source}"
        )
    
    # Check if format is supported
    if format.lower() not in importer.get_supported_formats():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format: {format}"
        )
    
    # Save the file
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(importer.import_dir, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Import the conversation
    try:
        result = importer.import_conversation(db, file_path, source, format)
        
        if "error" in result:
            # Clean up the file if import fails
            if os.path.exists(file_path):
                os.remove(file_path)
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        return result
    except Exception as e:
        # Clean up the file if import fails
        if os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing conversation: {str(e)}"
        )

@router.get("/sources", response_model=List[str])
def get_supported_sources():
    """
    Get a list of supported conversation sources.
    """
    importer = ConversationImporter()
    return importer.get_supported_sources()

@router.get("/formats", response_model=List[str])
def get_supported_formats():
    """
    Get a list of supported conversation formats.
    """
    importer = ConversationImporter()
    return importer.get_supported_formats()

@router.get("/conversations", response_model=ConversationListResponse)
def get_imported_conversations(
    db: Session = Depends(get_db)
):
    """
    Get all imported conversations.
    """
    from app.models import ImportedConversation
    
    conversations = db.query(ImportedConversation).all()
    return {"conversations": conversations}

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_imported_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """
    Get an imported conversation by ID.
    """
    from app.models import ImportedConversation, ConversationThought, Thought
    
    conversation = db.query(ImportedConversation).filter(
        ImportedConversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with ID {conversation_id} not found"
        )
    
    # Get conversation thoughts
    conversation_thoughts = db.query(ConversationThought).filter(
        ConversationThought.conversation_id == conversation_id
    ).order_by(ConversationThought.segment_index).all()
    
    # Get thoughts
    thoughts = []
    for ct in conversation_thoughts:
        thought = db.query(Thought).filter(Thought.id == ct.thought_id).first()
        if thought:
            thoughts.append({
                "id": thought.id,
                "content": thought.content,
                "role": ct.role,
                "segment_index": ct.segment_index,
                "created_at": thought.created_at
            })
    
    return {
        "id": conversation.id,
        "source": conversation.source,
        "format": conversation.format,
        "imported_at": conversation.imported_at,
        "original_file": conversation.original_file,
        "metadata": conversation.metadata,
        "thoughts": thoughts
    }

@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_imported_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an imported conversation.
    """
    from app.models import ImportedConversation, ConversationThought, Thought
    
    conversation = db.query(ImportedConversation).filter(
        ImportedConversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with ID {conversation_id} not found"
        )
    
    # Get conversation thoughts
    conversation_thoughts = db.query(ConversationThought).filter(
        ConversationThought.conversation_id == conversation_id
    ).all()
    
    # Delete thoughts
    for ct in conversation_thoughts:
        thought = db.query(Thought).filter(Thought.id == ct.thought_id).first()
        if thought:
            db.delete(thought)
        db.delete(ct)
    
    # Delete conversation
    db.delete(conversation)
    db.commit()
