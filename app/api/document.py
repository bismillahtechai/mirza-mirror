"""
API routes for document management in Mirza Mirror.
"""

import os
import shutil
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database import get_db
from app.models import Document
from app.services.document_service import DocumentService
from app.schemas.document import (
    DocumentResponse,
    DocumentListResponse
)

router = APIRouter(
    prefix="/api/document",
    tags=["document"],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process a document.
    """
    # Initialize document service
    document_service = DocumentService()
    
    # Check if file type is supported
    file_extension = os.path.splitext(file.filename)[1].lower().lstrip(".")
    if file_extension not in document_service.get_supported_formats():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file_extension}"
        )
    
    # Create a unique filename
    unique_filename = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(document_service.document_dir, unique_filename)
    
    # Save the file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Process the document
    try:
        document = document_service.process_document(db, file_path, file_extension)
        return document
    except Exception as e:
        # Clean up the file if processing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )

@router.get("/formats", response_model=List[str])
def get_supported_formats(
    db: Session = Depends(get_db)
):
    """
    Get a list of supported document formats.
    """
    document_service = DocumentService()
    return document_service.get_supported_formats()

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a document by ID.
    """
    document_service = DocumentService()
    document = document_service.get_document_by_id(db, document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found"
        )
    
    return document

@router.get("/thought/{thought_id}", response_model=DocumentListResponse)
def get_documents_for_thought(
    thought_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all documents associated with a thought.
    """
    document_service = DocumentService()
    documents = document_service.get_documents_for_thought(db, thought_id)
    
    return {"documents": documents}

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a document.
    """
    document_service = DocumentService()
    success = document_service.delete_document(db, document_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found"
        )
