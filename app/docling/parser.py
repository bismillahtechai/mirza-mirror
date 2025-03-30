"""
Document processing module for Mirza Mirror using Docling integration.
This module handles document parsing and analysis.
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from docling.document_converter import DocumentConverter
from docling.document import DoclingDocument

# Load environment variables
load_dotenv()

class DoclingManager:
    """
    Docling manager class that integrates Docling for document processing.
    Provides methods for parsing and analyzing documents.
    """
    
    def __init__(self):
        """
        Initialize the Docling manager.
        """
        self.converter = DocumentConverter()
        self.temp_dir = os.getenv("DOCLING_TEMP_DIR", "./temp_docs")
        
        # Create temp directory if it doesn't exist
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def parse_document(self, document_path: str) -> Dict[str, Any]:
        """
        Parse a document using Docling.
        
        Args:
            document_path: Path to the document
            
        Returns:
            Dict containing the parsed document information
        """
        try:
            # Convert the document using Docling
            result = self.converter.convert(document_path)
            
            # Get the Docling document
            docling_document = result.document
            
            # Return the document information
            return {
                "content": docling_document.export_to_markdown(),
                "docling_representation": docling_document.model_dump(),
                "metadata": self._extract_metadata(docling_document)
            }
        except Exception as e:
            return {
                "error": str(e),
                "content": None,
                "docling_representation": None,
                "metadata": None
            }
    
    def _extract_metadata(self, document: DoclingDocument) -> Dict[str, Any]:
        """
        Extract metadata from a Docling document.
        
        Args:
            document: Docling document
            
        Returns:
            Dict containing metadata
        """
        metadata = {}
        
        # Extract title
        if document.metadata and document.metadata.title:
            metadata["title"] = document.metadata.title
        
        # Extract authors
        if document.metadata and document.metadata.authors:
            metadata["authors"] = [author.name for author in document.metadata.authors]
        
        # Extract language
        if document.metadata and document.metadata.language:
            metadata["language"] = document.metadata.language
        
        # Extract creation date
        if document.metadata and document.metadata.creation_date:
            metadata["creation_date"] = document.metadata.creation_date
        
        # Extract modification date
        if document.metadata and document.metadata.modification_date:
            metadata["modification_date"] = document.metadata.modification_date
        
        # Extract page count
        if hasattr(document, "pages") and document.pages:
            metadata["page_count"] = len(document.pages)
        
        return metadata
    
    def extract_text(self, document_path: str) -> str:
        """
        Extract text from a document.
        
        Args:
            document_path: Path to the document
            
        Returns:
            Extracted text
        """
        try:
            # Parse the document
            result = self.parse_document(document_path)
            
            # Return the content
            return result.get("content", "")
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def get_supported_formats(self) -> List[str]:
        """
        Get a list of supported document formats.
        
        Returns:
            List of supported formats
        """
        return [
            "pdf",
            "docx",
            "xlsx",
            "pptx",
            "html",
            "txt",
            "md",
            "jpg",
            "jpeg",
            "png"
        ]
