import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the app directory to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agents import AgentService, TaggingAgent, LinkingAgent, ReflectionAgent, ActionAgent

class TestAgentService(unittest.TestCase):
    
    @patch('app.agents.openai')
    def setUp(self, mock_openai):
        self.mock_openai = mock_openai
        self.agent_service = AgentService()
    
    def test_initialization(self):
        """Test that the AgentService initializes correctly"""
        self.assertIsNotNone(self.agent_service)
        self.assertIsNotNone(self.agent_service.tagging_agent)
        self.assertIsNotNone(self.agent_service.linking_agent)
        self.assertIsNotNone(self.agent_service.reflection_agent)
        self.assertIsNotNone(self.agent_service.action_agent)
    
    @patch('app.agents.openai.agents')
    def test_tag_thought(self, mock_agents):
        """Test tagging a thought"""
        # Mock the agent response
        mock_agent = MagicMock()
        mock_agent.run.return_value = {'tags': ['productivity', 'idea', 'project']}
        mock_agents.Agent.return_value = mock_agent
        
        # Set up the tagging agent
        self.agent_service.tagging_agent = TaggingAgent()
        self.agent_service.tagging_agent.agent = mock_agent
        
        tags = self.agent_service.tag_thought("This is a thought about a new project idea")
        
        # Assert the thought was tagged
        self.assertEqual(len(tags), 3)
        self.assertIn('productivity', tags)
        self.assertIn('idea', tags)
        self.assertIn('project', tags)
        mock_agent.run.assert_called_once()
    
    @patch('app.agents.openai.agents')
    def test_link_thoughts(self, mock_agents):
        """Test linking thoughts"""
        # Mock the agent response
        mock_agent = MagicMock()
        mock_agent.run.return_value = {
            'links': [
                {'thought_id': '456', 'relationship': 'similar', 'strength': 0.85},
                {'thought_id': '789', 'relationship': 'continuation', 'strength': 0.75}
            ]
        }
        mock_agents.Agent.return_value = mock_agent
        
        # Mock the memory manager
        self.agent_service.memory_manager = MagicMock()
        self.agent_service.memory_manager.search_memories.return_value = [
            {'id': '456', 'content': 'Related thought 1', 'score': 0.85},
            {'id': '789', 'content': 'Related thought 2', 'score': 0.75}
        ]
        
        # Set up the linking agent
        self.agent_service.linking_agent = LinkingAgent()
        self.agent_service.linking_agent.agent = mock_agent
        
        links = self.agent_service.link_thought("This is a thought", "123")
        
        # Assert the thought was linked
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0]['thought_id'], '456')
        self.assertEqual(links[0]['relationship'], 'similar')
        self.assertEqual(links[1]['thought_id'], '789')
        self.assertEqual(links[1]['relationship'], 'continuation')
        mock_agent.run.assert_called_once()
        self.agent_service.memory_manager.search_memories.assert_called_once()
    
    @patch('app.agents.openai.agents')
    def test_generate_reflection(self, mock_agents):
        """Test generating a reflection"""
        # Mock the agent response
        mock_agent = MagicMock()
        mock_agent.run.return_value = {
            'summary': 'This is a summary of the thought',
            'emotion': 'excited',
            'insights': ['Insight 1', 'Insight 2']
        }
        mock_agents.Agent.return_value = mock_agent
        
        # Set up the reflection agent
        self.agent_service.reflection_agent = ReflectionAgent()
        self.agent_service.reflection_agent.agent = mock_agent
        
        reflection = self.agent_service.generate_reflection("This is a thought that I'm excited about")
        
        # Assert the reflection was generated
        self.assertEqual(reflection['summary'], 'This is a summary of the thought')
        self.assertEqual(reflection['emotion'], 'excited')
        self.assertEqual(len(reflection['insights']), 2)
        mock_agent.run.assert_called_once()
    
    @patch('app.agents.openai.agents')
    def test_extract_actions(self, mock_agents):
        """Test extracting actions"""
        # Mock the agent response
        mock_agent = MagicMock()
        mock_agent.run.return_value = {
            'actions': [
                {'content': 'Action 1', 'priority': 'high', 'due_date': '2025-04-05'},
                {'content': 'Action 2', 'priority': 'medium'}
            ]
        }
        mock_agents.Agent.return_value = mock_agent
        
        # Set up the action agent
        self.agent_service.action_agent = ActionAgent()
        self.agent_service.action_agent.agent = mock_agent
        
        actions = self.agent_service.extract_actions("I need to do Action 1 by next week and also Action 2")
        
        # Assert the actions were extracted
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]['content'], 'Action 1')
        self.assertEqual(actions[0]['priority'], 'high')
        self.assertEqual(actions[0]['due_date'], '2025-04-05')
        self.assertEqual(actions[1]['content'], 'Action 2')
        self.assertEqual(actions[1]['priority'], 'medium')
        mock_agent.run.assert_called_once()
    
    @patch('app.agents.openai.agents')
    @patch('app.agents.openai.mcp')
    def test_mcp_integration(self, mock_mcp, mock_agents):
        """Test MCP integration"""
        # Mock the MCP server
        mock_mcp_server = MagicMock()
        mock_mcp.MCPServer.return_value = mock_mcp_server
        
        # Create a new agent service to test MCP initialization
        agent_service = AgentService()
        
        # Assert MCP servers were created
        self.assertEqual(mock_mcp.MCPServer.call_count, 4)  # One for each agent
        
        # Test MCP context persistence
        mock_agent = MagicMock()
        mock_agents.Agent.return_value = mock_agent
        
        # Set up the tagging agent with MCP
        agent_service.tagging_agent = TaggingAgent()
        agent_service.tagging_agent.agent = mock_agent
        agent_service.tagging_agent.mcp_server = mock_mcp_server
        
        # Mock the MCP server get_context and update_context methods
        mock_mcp_server.get_context.return_value = {"previous_tags": ["tag1", "tag2"]}
        
        agent_service.tag_thought("This is a thought")
        
        # Assert the MCP context was accessed and updated
        mock_mcp_server.get_context.assert_called_once()
        mock_mcp_server.update_context.assert_called_once()

if __name__ == '__main__':
    unittest.main()
