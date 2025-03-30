"""
Document handling module for Mirza Mirror.
This module provides functionality for capturing and processing documents.
"""

import os
import uuid
import shutil
from typing import Dict, List, Optional, Any, BinaryIO
from fastapi import UploadFile
from PIL import Image
import pytesseract
from app.document import DoclingManager
from app.services.document_service import DocumentService

class DocumentHandler:
    """
    Document handler class that provides functionality for capturing and processing documents.
    """
    
    def __init__(self):
        """
        Initialize the document handler.
        """
        self.document_service = DocumentService()
        self.docling_manager = DoclingManager()
        self.upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
        self.document_dir = os.path.join(self.upload_dir, "documents")
        self.image_dir = os.path.join(self.upload_dir, "images")
        
        # Create directories if they don't exist
        os.makedirs(self.document_dir, exist_ok=True)
        os.makedirs(self.image_dir, exist_ok=True)
    
    async def handle_document_upload(self, file: UploadFile, db) -> Dict[str, Any]:
        """
        Handle document upload and processing.
        
        Args:
            file: Uploaded file
            db: Database session
            
        Returns:
            Dict containing the processed document information
        """
        # Check if file type is supported
        file_extension = os.path.splitext(file.filename)[1].lower().lstrip(".")
        if file_extension not in self.document_service.get_supported_formats():
            return {"error": f"Unsupported file type: {file_extension}"}
        
        # Create a unique filename
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(self.document_dir, unique_filename)
        
        # Save the file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            return {"error": f"Error saving file: {str(e)}"}
        
        # Process the document
        try:
            document = self.document_service.process_document(db, file_path, file_extension)
            return {
                "document_id": document.id,
                "thought_id": document.thought_id,
                "file_path": document.file_path,
                "file_type": document.file_type,
                "content": document.content[:200] + "..." if document.content and len(document.content) > 200 else document.content
            }
        except Exception as e:
            # Clean up the file if processing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return {"error": f"Error processing document: {str(e)}"}
    
    async def handle_image_upload(self, file: UploadFile, db) -> Dict[str, Any]:
        """
        Handle image upload and processing.
        
        Args:
            file: Uploaded image file
            db: Database session
            
        Returns:
            Dict containing the processed image information
        """
        # Check if file type is supported
        file_extension = os.path.splitext(file.filename)[1].lower().lstrip(".")
        if file_extension not in ["jpg", "jpeg", "png", "gif", "bmp", "tiff"]:
            return {"error": f"Unsupported image type: {file_extension}"}
        
        # Create a unique filename
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(self.image_dir, unique_filename)
        
        # Save the file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            return {"error": f"Error saving image: {str(e)}"}
        
        # Extract text from image using OCR
        try:
            extracted_text = self._extract_text_from_image(file_path)
            
            # Create a document with the extracted text
            document = self.document_service.process_document(db, file_path, file_extension)
            
            # Update the document content with the extracted text if needed
            if not document.content and extracted_text:
                document.content = extracted_text
                db.commit()
                db.refresh(document)
            
            return {
                "document_id": document.id,
                "thought_id": document.thought_id,
                "file_path": document.file_path,
                "file_type": document.file_type,
                "content": document.content[:200] + "..." if document.content and len(document.content) > 200 else document.content,
                "extracted_text": extracted_text[:200] + "..." if extracted_text and len(extracted_text) > 200 else extracted_text
            }
        except Exception as e:
            # Clean up the file if processing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return {"error": f"Error processing image: {str(e)}"}
    
    def _extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from an image using OCR.
        
        Args:
            image_path: Path to the image
            
        Returns:
            Extracted text
        """
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Extract text using pytesseract
            text = pytesseract.image_to_string(image)
            
            return text
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def handle_receipt(self, image_path: str) -> Dict[str, Any]:
        """
        Handle receipt image processing.
        
        Args:
            image_path: Path to the receipt image
            
        Returns:
            Dict containing the processed receipt information
        """
        # Extract text from receipt
        text = self._extract_text_from_image(image_path)
        
        # Parse receipt information (simplified version)
        lines = text.split('\n')
        
        # Extract basic receipt information
        merchant = lines[0] if lines else ""
        date = self._extract_date(text)
        total = self._extract_total(text)
        
        return {
            "merchant": merchant,
            "date": date,
            "total": total,
            "raw_text": text
        }
    
    def handle_business_card(self, image_path: str) -> Dict[str, Any]:
        """
        Handle business card image processing.
        
        Args:
            image_path: Path to the business card image
            
        Returns:
            Dict containing the processed business card information
        """
        # Extract text from business card
        text = self._extract_text_from_image(image_path)
        
        # Parse business card information (simplified version)
        lines = text.split('\n')
        
        # Extract basic business card information
        name = lines[0] if lines else ""
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "raw_text": text
        }
    
    def handle_screenshot(self, image_path: str) -> Dict[str, Any]:
        """
        Handle screenshot processing.
        
        Args:
            image_path: Path to the screenshot
            
        Returns:
            Dict containing the processed screenshot information
        """
        # Extract text from screenshot
        text = self._extract_text_from_image(image_path)
        
        return {
            "text": text,
            "image_path": image_path
        }
    
    def _extract_date(self, text: str) -> str:
        """
        Extract date from text.
        
        Args:
            text: Text to extract date from
            
        Returns:
            Extracted date or empty string
        """
        # Simple date extraction (would be more sophisticated in production)
        import re
        
        # Look for common date formats
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YYYY or DD/MM/YYYY
            r'\d{1,2}-\d{1,2}-\d{2,4}',  # MM-DD-YYYY or DD-MM-YYYY
            r'\d{1,2}\.\d{1,2}\.\d{2,4}'  # MM.DD.YYYY or DD.MM.YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return ""
    
    def _extract_total(self, text: str) -> str:
        """
        Extract total amount from text.
        
        Args:
            text: Text to extract total from
            
        Returns:
            Extracted total or empty string
        """
        # Simple total extraction (would be more sophisticated in production)
        import re
        
        # Look for common total amount patterns
        total_patterns = [
            r'Total:?\s*\$?\s*\d+\.\d{2}',
            r'Amount:?\s*\$?\s*\d+\.\d{2}',
            r'Sum:?\s*\$?\s*\d+\.\d{2}'
        ]
        
        for pattern in total_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        # Look for dollar amounts
        amount_pattern = r'\$\s*\d+\.\d{2}'
        amounts = re.findall(amount_pattern, text)
        
        # Return the last amount (often the total)
        if amounts:
            return amounts[-1]
        
        return ""
    
    def _extract_email(self, text: str) -> str:
        """
        Extract email from text.
        
        Args:
            text: Text to extract email from
            
        Returns:
            Extracted email or empty string
        """
        # Simple email extraction
        import re
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        
        if match:
            return match.group(0)
        
        return ""
    
    def _extract_phone(self, text: str) -> str:
        """
        Extract phone number from text.
        
        Args:
            text: Text to extract phone from
            
        Returns:
            Extracted phone or empty string
        """
        # Simple phone extraction
        import re
        
        phone_patterns = [
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',  # (123) 456-7890
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'    # 123-456-7890
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return ""
