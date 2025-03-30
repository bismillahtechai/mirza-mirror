import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the app directory to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.memory.memory_engine import MemoryManager

class TestMemoryManager(unittest.TestCase):
    
    @patch('app.memory.memory_engine.openai')
    def setUp(self, mock_openai):
        self.mock_openai = mock_openai
        self.memory_manager = MemoryManager()
    
    def test_initialization(self):
        """Test that the MemoryManager initializes correctly"""
        self.assertIsNotNone(self.memory_manager)
    
    @patch('app.memory.memory_engine.openai.Embedding.create')
    def test_add_memory(self, mock_embedding_create):
        """Test adding a memory"""
        # Mock the embedding response
        mock_embedding_create.return_value = {
            'data': [{'embedding': [0.1, 0.2, 0.3]}]
        }
        
        # Mock the mem0 add_memory method
        self.memory_manager.mem0_client = MagicMock()
        self.memory_manager.mem0_client.add_memory.return_value = {'id': '123'}
        
        result = self.memory_manager.add_memory(
            content="Test memory content",
            source="test",
            tags=["test", "memory"]
        )
        
        # Assert the memory was added
        self.assertEqual(result['id'], '123')
        self.memory_manager.mem0_client.add_memory.assert_called_once()
        mock_embedding_create.assert_called_once()
    
    @patch('app.memory.memory_engine.openai.Embedding.create')
    def test_search_memories(self, mock_embedding_create):
        """Test searching memories"""
        # Mock the embedding response
        mock_embedding_create.return_value = {
            'data': [{'embedding': [0.1, 0.2, 0.3]}]
        }
        
        # Mock the mem0 search_memories method
        self.memory_manager.mem0_client = MagicMock()
        self.memory_manager.mem0_client.search_memories.return_value = [
            {'id': '123', 'content': 'Test memory', 'score': 0.95}
        ]
        
        results = self.memory_manager.search_memories("test query")
        
        # Assert the search was performed
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], '123')
        self.memory_manager.mem0_client.search_memories.assert_called_once()
        mock_embedding_create.assert_called_once()
    
    def test_get_memory(self):
        """Test retrieving a specific memory"""
        # Mock the mem0 get_memory method
        self.memory_manager.mem0_client = MagicMock()
        self.memory_manager.mem0_client.get_memory.return_value = {
            'id': '123', 
            'content': 'Test memory content',
            'metadata': {'source': 'test', 'tags': ['test', 'memory']}
        }
        
        memory = self.memory_manager.get_memory('123')
        
        # Assert the memory was retrieved
        self.assertEqual(memory['id'], '123')
        self.assertEqual(memory['content'], 'Test memory content')
        self.memory_manager.mem0_client.get_memory.assert_called_once_with('123')

if __name__ == '__main__':
    unittest.main()
