import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the app directory to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.memory import router as memory_router
from app.api.capture import router as capture_router
from app.api.documents import router as documents_router
from app.api.import_conversation import router as import_router
from app.api.agents import router as agents_router

class TestAPIEndpoints(unittest.TestCase):
    
    @patch('app.api.memory.MemoryManager')
    def test_memory_endpoints(self, mock_memory_manager):
        """Test memory API endpoints"""
        # Mock the memory manager
        mock_memory_instance = MagicMock()
        mock_memory_manager.return_value = mock_memory_instance
        
        # Mock the memory manager methods
        mock_memory_instance.get_memory.return_value = {'id': '123', 'content': 'Test memory'}
        mock_memory_instance.search_memories.return_value = [{'id': '123', 'content': 'Test memory'}]
        mock_memory_instance.add_memory.return_value = {'id': '123'}
        
        # Test the endpoints
        self.assertIn('/memories/{memory_id}', [route.path for route in memory_router.routes])
        self.assertIn('/memories/search', [route.path for route in memory_router.routes])
        self.assertIn('/memories', [route.path for route in memory_router.routes])
    
    @patch('app.api.capture.CaptureProcessor')
    def test_capture_endpoints(self, mock_capture_processor):
        """Test capture API endpoints"""
        # Mock the capture processor
        mock_capture_instance = MagicMock()
        mock_capture_processor.return_value = mock_capture_instance
        
        # Mock the capture processor methods
        mock_capture_instance.process_text_thought.return_value = {'id': '123', 'content': 'Test thought'}
        mock_capture_instance.process_voice_thought.return_value = {'id': '123', 'content': 'Test voice thought'}
        mock_capture_instance.search_thoughts.return_value = [{'id': '123', 'content': 'Test thought'}]
        
        # Test the endpoints
        self.assertIn('/thoughts', [route.path for route in capture_router.routes])
        self.assertIn('/thoughts/voice', [route.path for route in capture_router.routes])
        self.assertIn('/thoughts/search', [route.path for route in capture_router.routes])
        self.assertIn('/thoughts/{thought_id}', [route.path for route in capture_router.routes])
    
    @patch('app.api.documents.DocumentHandler')
    def test_document_endpoints(self, mock_document_handler):
        """Test document API endpoints"""
        # Mock the document handler
        mock_document_instance = MagicMock()
        mock_document_handler.return_value = mock_document_instance
        
        # Mock the document handler methods
        mock_document_instance.process_document.return_value = {'id': '123', 'content': 'Test document'}
        mock_document_instance.get_document.return_value = {'id': '123', 'content': 'Test document'}
        
        # Test the endpoints
        self.assertIn('/documents', [route.path for route in documents_router.routes])
        self.assertIn('/documents/{document_id}', [route.path for route in documents_router.routes])
    
    @patch('app.api.import_conversation.ConversationImporter')
    def test_import_endpoints(self, mock_importer):
        """Test import API endpoints"""
        # Mock the conversation importer
        mock_importer_instance = MagicMock()
        mock_importer.return_value = mock_importer_instance
        
        # Mock the importer methods
        mock_importer_instance.import_from_markdown.return_value = [{'role': 'user', 'content': 'Test message'}]
        mock_importer_instance.import_from_json.return_value = [{'role': 'user', 'content': 'Test message'}]
        
        # Test the endpoints
        self.assertIn('/import', [route.path for route in import_router.routes])
    
    @patch('app.api.agents.AgentService')
    def test_agent_endpoints(self, mock_agent_service):
        """Test agent API endpoints"""
        # Mock the agent service
        mock_agent_instance = MagicMock()
        mock_agent_service.return_value = mock_agent_instance
        
        # Mock the agent service methods
        mock_agent_instance.tag_thought.return_value = ['tag1', 'tag2']
        mock_agent_instance.link_thought.return_value = [{'thought_id': '456', 'relationship': 'similar'}]
        mock_agent_instance.generate_reflection.return_value = {'summary': 'Test summary', 'emotion': 'neutral'}
        mock_agent_instance.extract_actions.return_value = [{'content': 'Action 1', 'priority': 'high'}]
        
        # Test the endpoints
        self.assertIn('/agents/tag', [route.path for route in agents_router.routes])
        self.assertIn('/agents/link', [route.path for route in agents_router.routes])
        self.assertIn('/agents/reflect', [route.path for route in agents_router.routes])
        self.assertIn('/agents/actions', [route.path for route in agents_router.routes])

if __name__ == '__main__':
    unittest.main()
