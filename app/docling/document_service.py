"""
Document service for Mirza Mirror using Docling integration.
This service provides higher-level functions for document management.
"""

import os
import uuid
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from app.document import DoclingManager
from app.models import Document, Thought
from app.database import get_db

class DocumentService:
    """
    Service class that provides document management functionality.
    Integrates Docling with the database models.
    """
    
    def __init__(self):
        """
        Initialize the document service.
        """
        self.docling_manager = DoclingManager()
        self.document_dir = os.getenv("DOCUMENT_DIR", "./uploads/documents")
        
        # Create document directory if it doesn't exist
        os.makedirs(self.document_dir, exist_ok=True)
    
    def process_document(self, db: Session, file_path: str, file_type: str) -> Document:
        """
        Process a document and store it in the database.
        
        Args:
            db: Database session
            file_path: Path to the document file
            file_type: Type of the document
            
        Returns:
            Document object
        """
        # Parse the document using Docling
        parse_result = self.docling_manager.parse_document(file_path)
        
        # Create a thought from the document content
        thought = Thought(
            id=str(uuid.uuid4()),
            content=parse_result.get("content", ""),
            source="document",
            document_file=file_path,
            summary=self._generate_summary(parse_result.get("content", "")),
            metadata=parse_result.get("metadata", {})
        )
        
        db.add(thought)
        db.commit()
        db.refresh(thought)
        
        # Create a document record
        document = Document(
            id=str(uuid.uuid4()),
            thought_id=thought.id,
            file_path=file_path,
            file_type=file_type,
            content=parse_result.get("content", ""),
            docling_representation=parse_result.get("docling_representation", {}),
            created_at=thought.created_at,
            updated_at=thought.updated_at
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return document
    
    def _generate_summary(self, content: str, max_length: int = 200) -> str:
        """
        Generate a summary of the document content.
        
        Args:
            content: Document content
            max_length: Maximum length of the summary
            
        Returns:
            Summary of the document
        """
        # Simple summary generation - first few characters
        if not content:
            return ""
        
        # Remove extra whitespace
        content = " ".join(content.split())
        
        # Truncate to max_length
        if len(content) > max_length:
            return content[:max_length] + "..."
        
        return content
    
    def get_document_by_id(self, db: Session, document_id: str) -> Optional[Document]:
        """
        Get a document by ID.
        
        Args:
            db: Database session
            document_id: ID of the document
            
        Returns:
            Document object or None if not found
        """
        return db.query(Document).filter(Document.id == document_id).first()
    
    def get_documents_for_thought(self, db: Session, thought_id: str) -> List[Document]:
        """
        Get all documents associated with a thought.
        
        Args:
            db: Database session
            thought_id: ID of the thought
            
        Returns:
            List of Document objects
        """
        return db.query(Document).filter(Document.thought_id == thought_id).all()
    
    def get_supported_formats(self) -> List[str]:
        """
        Get a list of supported document formats.
        
        Returns:
            List of supported formats
        """
        return self.docling_manager.get_supported_formats()
    
    def delete_document(self, db: Session, document_id: str) -> bool:
        """
        Delete a document.
        
        Args:
            db: Database session
            document_id: ID of the document to delete
            
        Returns:
            True if successful, False otherwise
        """
        document = self.get_document_by_id(db, document_id)
        if not document:
            return False
        
        # Delete the document file if it exists
        if os.path.exists(document.file_path):
            try:
                os.remove(document.file_path)
            except Exception:
                pass
        
        # Delete the document record
        db.delete(document)
        db.commit()
        
        return True
