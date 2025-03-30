import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the app directory to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.docling.parser import DoclingManager

class TestDoclingManager(unittest.TestCase):
    
    def setUp(self):
        self.docling_manager = DoclingManager()
    
    def test_initialization(self):
        """Test that the DoclingManager initializes correctly"""
        self.assertIsNotNone(self.docling_manager)
    
    @patch('app.docling.parser.docling')
    def test_parse_document(self, mock_docling):
        """Test parsing a document"""
        # Mock the docling parse method
        mock_docling.parse.return_value = {
            'content': 'Test document content',
            'metadata': {'title': 'Test Document', 'type': 'text/plain'}
        }
        
        result = self.docling_manager.parse_document(
            file_path="test_document.txt",
            document_type="text"
        )
        
        # Assert the document was parsed
        self.assertEqual(result['content'], 'Test document content')
        self.assertEqual(result['metadata']['title'], 'Test Document')
        mock_docling.parse.assert_called_once()
    
    @patch('app.docling.parser.docling')
    def test_extract_metadata(self, mock_docling):
        """Test extracting metadata from a document"""
        # Mock the docling extract_metadata method
        mock_docling.extract_metadata.return_value = {
            'title': 'Test Document',
            'author': 'Test Author',
            'created_date': '2025-03-30',
            'type': 'text/plain'
        }
        
        metadata = self.docling_manager.extract_metadata("test_document.txt")
        
        # Assert the metadata was extracted
        self.assertEqual(metadata['title'], 'Test Document')
        self.assertEqual(metadata['author'], 'Test Author')
        mock_docling.extract_metadata.assert_called_once_with("test_document.txt")
    
    @patch('app.docling.parser.docling')
    def test_analyze_document(self, mock_docling):
        """Test analyzing a document for key concepts"""
        # Mock the docling analyze method
        mock_docling.analyze.return_value = {
            'key_concepts': ['concept1', 'concept2'],
            'summary': 'This is a test document summary',
            'sentiment': 'neutral'
        }
        
        analysis = self.docling_manager.analyze_document("Test document content")
        
        # Assert the document was analyzed
        self.assertEqual(len(analysis['key_concepts']), 2)
        self.assertEqual(analysis['summary'], 'This is a test document summary')
        mock_docling.analyze.assert_called_once()

if __name__ == '__main__':
    unittest.main()
