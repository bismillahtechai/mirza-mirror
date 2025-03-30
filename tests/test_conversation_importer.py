import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add the app directory to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.import_conversation import ConversationImporter

class TestConversationImporter(unittest.TestCase):
    
    def setUp(self):
        self.importer = ConversationImporter()
    
    def test_initialization(self):
        """Test that the ConversationImporter initializes correctly"""
        self.assertIsNotNone(self.importer)
    
    @patch('app.import_conversation.open')
    def test_import_chatgpt_markdown(self, mock_open):
        """Test importing a ChatGPT conversation from markdown"""
        # Mock the open function to return a markdown file
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = """
# Conversation with ChatGPT

#### You:
Hello, how are you?

#### ChatGPT:
I'm doing well, thank you for asking! How can I help you today?

#### You:
What's the weather like?

#### ChatGPT:
I don't have real-time data about the current weather. To get accurate weather information, you could check a weather website or app, or ask a virtual assistant with internet access.
"""
        mock_open.return_value = mock_file
        
        # Mock the memory manager
        self.importer.memory_manager = MagicMock()
        self.importer.memory_manager.add_memory.return_value = {'id': '123'}
        
        result = self.importer.import_from_markdown("test_conversation.md", "chatgpt")
        
        # Assert the conversation was imported
        self.assertEqual(len(result), 2)  # 2 exchanges
        self.assertEqual(result[0]['role'], 'user')
        self.assertEqual(result[0]['content'], 'Hello, how are you?')
        self.assertEqual(result[1]['role'], 'assistant')
        self.assertEqual(result[1]['content'], "I'm doing well, thank you for asking! How can I help you today?")
        
        # Assert memories were added
        self.assertEqual(self.importer.memory_manager.add_memory.call_count, 4)  # 4 messages
    
    @patch('app.import_conversation.open')
    def test_import_chatgpt_json(self, mock_open):
        """Test importing a ChatGPT conversation from JSON"""
        # Mock the open function to return a JSON file
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = json.dumps({
            "title": "Test Conversation",
            "create_time": 1648224000,
            "update_time": 1648224100,
            "mapping": {
                "abc123": {
                    "id": "abc123",
                    "message": {
                        "content": {
                            "parts": ["Hello, how are you?"],
                            "role": "user"
                        },
                        "create_time": 1648224000
                    }
                },
                "def456": {
                    "id": "def456",
                    "message": {
                        "content": {
                            "parts": ["I'm doing well, thank you for asking! How can I help you today?"],
                            "role": "assistant"
                        },
                        "create_time": 1648224050
                    }
                }
            }
        })
        mock_open.return_value = mock_file
        
        # Mock the memory manager
        self.importer.memory_manager = MagicMock()
        self.importer.memory_manager.add_memory.return_value = {'id': '123'}
        
        result = self.importer.import_from_json("test_conversation.json", "chatgpt")
        
        # Assert the conversation was imported
        self.assertEqual(len(result), 2)  # 2 messages
        self.assertEqual(result[0]['role'], 'user')
        self.assertEqual(result[0]['content'], 'Hello, how are you?')
        self.assertEqual(result[1]['role'], 'assistant')
        self.assertEqual(result[1]['content'], "I'm doing well, thank you for asking! How can I help you today?")
        
        # Assert memories were added
        self.assertEqual(self.importer.memory_manager.add_memory.call_count, 2)  # 2 messages
    
    @patch('app.import_conversation.open')
    def test_import_claude_json(self, mock_open):
        """Test importing a Claude conversation from JSON"""
        # Mock the open function to return a JSON file
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = json.dumps({
            "title": "Test Claude Conversation",
            "conversations": [
                {
                    "id": "conv_123",
                    "messages": [
                        {
                            "id": "msg_1",
                            "role": "human",
                            "content": "Hello Claude, how are you?",
                            "timestamp": 1648224000
                        },
                        {
                            "id": "msg_2",
                            "role": "assistant",
                            "content": "I'm Claude, an AI assistant created by Anthropic. I'm functioning well and ready to help you with information, tasks, or discussions. How can I assist you today?",
                            "timestamp": 1648224050
                        }
                    ]
                }
            ]
        })
        mock_open.return_value = mock_file
        
        # Mock the memory manager
        self.importer.memory_manager = MagicMock()
        self.importer.memory_manager.add_memory.return_value = {'id': '123'}
        
        result = self.importer.import_from_json("test_conversation.json", "claude")
        
        # Assert the conversation was imported
        self.assertEqual(len(result), 2)  # 2 messages
        self.assertEqual(result[0]['role'], 'user')
        self.assertEqual(result[0]['content'], 'Hello Claude, how are you?')
        self.assertEqual(result[1]['role'], 'assistant')
        self.assertTrue("I'm Claude" in result[1]['content'])
        
        # Assert memories were added
        self.assertEqual(self.importer.memory_manager.add_memory.call_count, 2)  # 2 messages

if __name__ == '__main__':
    unittest.main()
