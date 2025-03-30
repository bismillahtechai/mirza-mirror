"""
API routes for document handling in Mirza Mirror.
"""

import os
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.handlers.document_handler import DocumentHandler
from app.schemas.document import (
    DocumentResponse,
    DocumentListResponse,
    ReceiptResponse,
    BusinessCardResponse,
    ScreenshotResponse
)

router = APIRouter(
    prefix="/api/documents",
    tags=["documents"],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    document_type: str = Form("general"),
    db: Session = Depends(get_db)
):
    """
    Upload and process a document.
    
    Args:
        file: The document file to upload
        document_type: Type of document (general, receipt, business_card, screenshot)
        db: Database session
    """
    document_handler = DocumentHandler()
    
    # Handle different document types
    if document_type == "general":
        result = await document_handler.handle_document_upload(file, db)
    elif document_type == "receipt":
        # First handle as image, then process as receipt
        image_result = await document_handler.handle_image_upload(file, db)
        if "error" in image_result:
            return image_result
        
        # Process as receipt in background
        background_tasks.add_task(
            process_receipt_background,
            image_result["file_path"],
            image_result["document_id"],
            db
        )
        
        return {
            **image_result,
            "processing_status": "Receipt processing started in background"
        }
    elif document_type == "business_card":
        # First handle as image, then process as business card
        image_result = await document_handler.handle_image_upload(file, db)
        if "error" in image_result:
            return image_result
        
        # Process as business card in background
        background_tasks.add_task(
            process_business_card_background,
            image_result["file_path"],
            image_result["document_id"],
            db
        )
        
        return {
            **image_result,
            "processing_status": "Business card processing started in background"
        }
    elif document_type == "screenshot":
        # Handle as image
        return await document_handler.handle_image_upload(file, db)
    else:
        return {"error": f"Unsupported document type: {document_type}"}
    
    return result

@router.get("/receipt/{document_id}", response_model=ReceiptResponse)
async def get_receipt_data(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get receipt data for a document.
    
    Args:
        document_id: ID of the document
        db: Database session
    """
    from app.models import Document
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found"
        )
    
    # Check if receipt data exists in metadata
    if not document.docling_representation or "receipt_data" not in document.docling_representation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receipt data not found for document with ID {document_id}"
        )
    
    return document.docling_representation["receipt_data"]

@router.get("/business-card/{document_id}", response_model=BusinessCardResponse)
async def get_business_card_data(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get business card data for a document.
    
    Args:
        document_id: ID of the document
        db: Database session
    """
    from app.models import Document
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found"
        )
    
    # Check if business card data exists in metadata
    if not document.docling_representation or "business_card_data" not in document.docling_representation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Business card data not found for document with ID {document_id}"
        )
    
    return document.docling_representation["business_card_data"]

@router.get("/screenshot/{document_id}", response_model=ScreenshotResponse)
async def get_screenshot_data(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get screenshot data for a document.
    
    Args:
        document_id: ID of the document
        db: Database session
    """
    from app.models import Document
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found"
        )
    
    return {
        "document_id": document.id,
        "text": document.content,
        "image_path": document.file_path
    }

# Background processing functions
def process_receipt_background(file_path: str, document_id: str, db: Session):
    """
    Process receipt in background.
    
    Args:
        file_path: Path to the receipt image
        document_id: ID of the document
        db: Database session
    """
    from app.models import Document
    
    document_handler = DocumentHandler()
    receipt_data = document_handler.handle_receipt(file_path)
    
    # Update document with receipt data
    document = db.query(Document).filter(Document.id == document_id).first()
    if document:
        if not document.docling_representation:
            document.docling_representation = {}
        
        document.docling_representation["receipt_data"] = receipt_data
        db.commit()

def process_business_card_background(file_path: str, document_id: str, db: Session):
    """
    Process business card in background.
    
    Args:
        file_path: Path to the business card image
        document_id: ID of the document
        db: Database session
    """
    from app.models import Document
    
    document_handler = DocumentHandler()
    business_card_data = document_handler.handle_business_card(file_path)
    
    # Update document with business card data
    document = db.query(Document).filter(Document.id == document_id).first()
    if document:
        if not document.docling_representation:
            document.docling_representation = {}
        
        document.docling_representation["business_card_data"] = business_card_data
        db.commit()
