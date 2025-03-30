import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the app directory to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.capture import CaptureProcessor

class TestCaptureProcessor(unittest.TestCase):
    
    def setUp(self):
        self.capture_processor = CaptureProcessor()
    
    def test_initialization(self):
        """Test that the CaptureProcessor initializes correctly"""
        self.assertIsNotNone(self.capture_processor)
    
    @patch('app.capture.openai')
    def test_process_text_thought(self, mock_openai):
        """Test processing a text thought"""
        # Mock the memory manager
        self.capture_processor.memory_manager = MagicMock()
        self.capture_processor.memory_manager.add_memory.return_value = {'id': '123'}
        
        # Mock the agent service
        self.capture_processor.agent_service = MagicMock()
        self.capture_processor.agent_service.tag_thought.return_value = ['tag1', 'tag2']
        self.capture_processor.agent_service.extract_actions.return_value = [
            {'content': 'Action 1', 'priority': 'high'}
        ]
        self.capture_processor.agent_service.generate_reflection.return_value = {
            'summary': 'Test summary',
            'emotion': 'neutral'
        }
        
        result = self.capture_processor.process_text_thought(
            content="This is a test thought",
            source="web_app"
        )
        
        # Assert the thought was processed
        self.assertEqual(result['id'], '123')
        self.capture_processor.memory_manager.add_memory.assert_called_once()
        self.capture_processor.agent_service.tag_thought.assert_called_once()
        self.capture_processor.agent_service.extract_actions.assert_called_once()
        self.capture_processor.agent_service.generate_reflection.assert_called_once()
    
    @patch('app.capture.openai')
    @patch('app.capture.whisper')
    def test_process_voice_thought(self, mock_whisper, mock_openai):
        """Test processing a voice thought"""
        # Mock the whisper transcription
        mock_whisper.transcribe.return_value = {
            'text': 'This is a transcribed voice thought'
        }
        
        # Mock the memory manager
        self.capture_processor.memory_manager = MagicMock()
        self.capture_processor.memory_manager.add_memory.return_value = {'id': '123'}
        
        # Mock the agent service
        self.capture_processor.agent_service = MagicMock()
        self.capture_processor.agent_service.tag_thought.return_value = ['tag1', 'tag2']
        self.capture_processor.agent_service.extract_actions.return_value = [
            {'content': 'Action 1', 'priority': 'high'}
        ]
        self.capture_processor.agent_service.generate_reflection.return_value = {
            'summary': 'Test summary',
            'emotion': 'neutral'
        }
        
        # Create a mock audio file
        mock_audio_file = MagicMock()
        
        result = self.capture_processor.process_voice_thought(
            audio_file=mock_audio_file,
            source="ios_app"
        )
        
        # Assert the voice thought was processed
        self.assertEqual(result['id'], '123')
        self.assertEqual(result['content'], 'This is a transcribed voice thought')
        mock_whisper.transcribe.assert_called_once()
        self.capture_processor.memory_manager.add_memory.assert_called_once()
        self.capture_processor.agent_service.tag_thought.assert_called_once()
        self.capture_processor.agent_service.extract_actions.assert_called_once()
        self.capture_processor.agent_service.generate_reflection.assert_called_once()
    
    def test_search_thoughts(self):
        """Test searching thoughts"""
        # Mock the memory manager
        self.capture_processor.memory_manager = MagicMock()
        self.capture_processor.memory_manager.search_memories.return_value = [
            {'id': '123', 'content': 'Test thought', 'score': 0.95}
        ]
        
        results = self.capture_processor.search_thoughts("test query")
        
        # Assert the search was performed
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], '123')
        self.capture_processor.memory_manager.search_memories.assert_called_once_with("test query")

if __name__ == '__main__':
    unittest.main()
