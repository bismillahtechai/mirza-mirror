"""
OpenAI Agents with MCP integration for Mirza Mirror.
This module implements intelligent agents using OpenAI Agents SDK with Model Context Protocol.
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from agents import Agent, Runner, Tool, AgentResponse
from agents.mcp import MCPServer

# Load environment variables
load_dotenv()

class AgentManager:
    """
    Agent manager class that implements OpenAI Agents with MCP integration.
    Provides specialized agents for different tasks in the thought externalization system.
    """
    
    def __init__(self):
        """
        Initialize the agent manager with specialized agents.
        """
        # Initialize MCP servers for each agent type
        self.tagging_mcp = MCPServer(name="tagging_context")
        self.linking_mcp = MCPServer(name="linking_context")
        self.reflection_mcp = MCPServer(name="reflection_context")
        self.action_mcp = MCPServer(name="action_context")
        
        # Initialize agents with their respective MCP servers
        self.tagging_agent = self._create_tagging_agent()
        self.linking_agent = self._create_linking_agent()
        self.reflection_agent = self._create_reflection_agent()
        self.action_agent = self._create_action_agent()
    
    def _create_tagging_agent(self) -> Agent:
        """
        Create a tagging agent with MCP integration.
        
        Returns:
            Agent for tagging thoughts
        """
        instructions = """
        You are a tagging agent for the Mirza Mirror thought externalization system.
        Your task is to analyze thought content and generate relevant tags.
        
        Guidelines for tagging:
        1. Identify key topics, concepts, and themes in the thought
        2. Extract emotional content and sentiment
        3. Recognize project references and action items
        4. Identify people, places, and organizations
        5. Tag temporal references (today, tomorrow, next week)
        6. Recognize priority indicators (urgent, important)
        
        For each tag, provide a confidence score between 0 and 1.
        """
        
        # Define tools for the tagging agent
        tools = [
            Tool(
                name="generate_tags",
                description="Generate tags for a thought",
                function=lambda thought_content: {
                    "tags": self._extract_tags(thought_content)
                }
            )
        ]
        
        # Create the agent with MCP integration
        return Agent(
            name="TaggingAgent",
            instructions=instructions,
            tools=tools,
            mcp=self.tagging_mcp
        )
    
    def _create_linking_agent(self) -> Agent:
        """
        Create a linking agent with MCP integration.
        
        Returns:
            Agent for linking related thoughts
        """
        instructions = """
        You are a linking agent for the Mirza Mirror thought externalization system.
        Your task is to analyze thought content and identify relationships with other thoughts.
        
        Guidelines for linking:
        1. Identify semantic similarities between thoughts
        2. Recognize when a thought is a continuation of another
        3. Detect contradictions or opposing viewpoints
        4. Identify when a thought is inspired by or references another
        5. Recognize thoughts that belong to the same project or theme
        
        For each link, provide a relationship type and a strength score between 0 and 1.
        """
        
        # Define tools for the linking agent
        tools = [
            Tool(
                name="find_related_thoughts",
                description="Find thoughts related to the given thought",
                function=lambda thought_content, existing_thoughts: {
                    "links": self._find_related_thoughts(thought_content, existing_thoughts)
                }
            )
        ]
        
        # Create the agent with MCP integration
        return Agent(
            name="LinkingAgent",
            instructions=instructions,
            tools=tools,
            mcp=self.linking_mcp
        )
    
    def _create_reflection_agent(self) -> Agent:
        """
        Create a reflection agent with MCP integration.
        
        Returns:
            Agent for generating reflections on thoughts
        """
        instructions = """
        You are a reflection agent for the Mirza Mirror thought externalization system.
        Your task is to analyze thought content and generate insights, patterns, and summaries.
        
        Guidelines for reflection:
        1. Identify recurring themes and patterns across thoughts
        2. Recognize emotional patterns and changes over time
        3. Summarize complex or lengthy thoughts
        4. Extract key insights and learnings
        5. Identify potential blind spots or alternative perspectives
        6. Connect thoughts to broader life goals or values
        
        Provide reflections that are insightful, empathetic, and actionable.
        """
        
        # Define tools for the reflection agent
        tools = [
            Tool(
                name="generate_reflection",
                description="Generate a reflection based on thought content",
                function=lambda thought_content, related_thoughts=None: {
                    "reflection": self._generate_reflection(thought_content, related_thoughts)
                }
            ),
            Tool(
                name="summarize_thought",
                description="Generate a concise summary of a thought",
                function=lambda thought_content: {
                    "summary": self._summarize_thought(thought_content)
                }
            )
        ]
        
        # Create the agent with MCP integration
        return Agent(
            name="ReflectionAgent",
            instructions=instructions,
            tools=tools,
            mcp=self.reflection_mcp
        )
    
    def _create_action_agent(self) -> Agent:
        """
        Create an action agent with MCP integration.
        
        Returns:
            Agent for extracting actionable items from thoughts
        """
        instructions = """
        You are an action agent for the Mirza Mirror thought externalization system.
        Your task is to analyze thought content and extract actionable items.
        
        Guidelines for action extraction:
        1. Identify explicit tasks and to-dos
        2. Recognize implicit actions and next steps
        3. Extract deadlines and temporal constraints
        4. Determine priority levels (high, medium, low)
        5. Identify dependencies between actions
        6. Recognize the context or project for each action
        
        For each action, provide the action content, priority, and due date if available.
        """
        
        # Define tools for the action agent
        tools = [
            Tool(
                name="extract_actions",
                description="Extract actionable items from thought content",
                function=lambda thought_content: {
                    "actions": self._extract_actions(thought_content)
                }
            )
        ]
        
        # Create the agent with MCP integration
        return Agent(
            name="ActionAgent",
            instructions=instructions,
            tools=tools,
            mcp=self.action_mcp
        )
    
    def process_thought(self, thought_content: str, existing_thoughts: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Process a thought using all agents.
        
        Args:
            thought_content: Content of the thought
            existing_thoughts: List of existing thoughts for context
            
        Returns:
            Dict containing the processed thought information
        """
        # Process with tagging agent
        tagging_result = self.generate_tags(thought_content)
        
        # Process with linking agent if existing thoughts are provided
        linking_result = {}
        if existing_thoughts:
            linking_result = self.find_related_thoughts(thought_content, existing_thoughts)
        
        # Process with reflection agent
        reflection_result = self.generate_reflection(thought_content, existing_thoughts)
        
        # Process with action agent
        action_result = self.extract_actions(thought_content)
        
        # Combine results
        return {
            "tags": tagging_result.get("tags", []),
            "links": linking_result.get("links", []),
            "reflection": reflection_result.get("reflection", ""),
            "summary": reflection_result.get("summary", ""),
            "actions": action_result.get("actions", [])
        }
    
    def generate_tags(self, thought_content: str) -> Dict[str, Any]:
        """
        Generate tags for a thought.
        
        Args:
            thought_content: Content of the thought
            
        Returns:
            Dict containing the generated tags
        """
        try:
            # Run the tagging agent
            result = Runner.run_sync(
                self.tagging_agent,
                f"Generate tags for the following thought: {thought_content}"
            )
            
            # Extract tags from the result
            if hasattr(result, "tool_calls") and result.tool_calls:
                for tool_call in result.tool_calls:
                    if tool_call.name == "generate_tags" and tool_call.result:
                        return tool_call.result
            
            # If no tool calls or results, extract from final output
            return {"tags": self._extract_tags_from_text(result.final_output)}
        except Exception as e:
            return {"error": f"Error generating tags: {str(e)}"}
    
    def find_related_thoughts(self, thought_content: str, existing_thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Find thoughts related to the given thought.
        
        Args:
            thought_content: Content of the thought
            existing_thoughts: List of existing thoughts
            
        Returns:
            Dict containing the related thoughts
        """
        try:
            # Format existing thoughts for the agent
            formatted_thoughts = "\n\n".join([
                f"Thought {i+1} (ID: {thought.get('id', 'unknown')}):\n{thought.get('content', '')}"
                for i, thought in enumerate(existing_thoughts)
            ])
            
            # Run the linking agent
            result = Runner.run_sync(
                self.linking_agent,
                f"Find thoughts related to the following thought:\n\nNew Thought:\n{thought_content}\n\nExisting Thoughts:\n{formatted_thoughts}"
            )
            
            # Extract links from the result
            if hasattr(result, "tool_calls") and result.tool_calls:
                for tool_call in result.tool_calls:
                    if tool_call.name == "find_related_thoughts" and tool_call.result:
                        return tool_call.result
            
            # If no tool calls or results, extract from final output
            return {"links": self._extract_links_from_text(result.final_output, existing_thoughts)}
        except Exception as e:
            return {"error": f"Error finding related thoughts: {str(e)}"}
    
    def generate_reflection(self, thought_content: str, related_thoughts: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Generate a reflection based on thought content.
        
        Args:
            thought_content: Content of the thought
            related_thoughts: List of related thoughts for context
            
        Returns:
            Dict containing the generated reflection
        """
        try:
            # Format related thoughts for the agent if provided
            context = ""
            if related_thoughts:
                formatted_thoughts = "\n\n".join([
                    f"Related Thought {i+1}:\n{thought.get('content', '')}"
                    for i, thought in enumerate(related_thoughts)
                ])
                context = f"\n\nContext from related thoughts:\n{formatted_thoughts}"
            
            # Run the reflection agent
            result = Runner.run_sync(
                self.reflection_agent,
                f"Generate a reflection and summary for the following thought:{context}\n\nThought:\n{thought_content}"
            )
            
            # Extract reflection from the result
            reflection = ""
            summary = ""
            
            if hasattr(result, "tool_calls") and result.tool_calls:
                for tool_call in result.tool_calls:
                    if tool_call.name == "generate_reflection" and tool_call.result:
                        reflection = tool_call.result.get("reflection", "")
                    elif tool_call.name == "summarize_thought" and tool_call.result:
                        summary = tool_call.result.get("summary", "")
            
            # If no tool calls or results, extract from final output
            if not reflection and not summary:
                output_parts = result.final_output.split("\n\n", 1)
                if len(output_parts) > 1:
                    summary = output_parts[0]
                    reflection = output_parts[1]
                else:
                    reflection = result.final_output
            
            return {
                "reflection": reflection,
                "summary": summary
            }
        except Exception as e:
            return {"error": f"Error generating reflection: {str(e)}"}
    
    def extract_actions(self, thought_content: str) -> Dict[str, Any]:
        """
        Extract actionable items from thought content.
        
        Args:
            thought_content: Content of the thought
            
        Returns:
            Dict containing the extracted actions
        """
        try:
            # Run the action agent
            result = Runner.run_sync(
                self.action_agent,
                f"Extract actionable items from the following thought:\n\n{thought_content}"
            )
            
            # Extract actions from the result
            if hasattr(result, "tool_calls") and result.tool_calls:
                for tool_call in result.tool_calls:
                    if tool_call.name == "extract_actions" and tool_call.result:
                        return tool_call.result
            
            # If no tool calls or results, extract from final output
            return {"actions": self._extract_actions_from_text(result.final_output)}
        except Exception as e:
            return {"error": f"Error extracting actions: {str(e)}"}
    
    def _extract_tags(self, thought_content: str) -> List[Dict[str, Any]]:
        """
        Extract tags from thought content.
        
        Args:
            thought_content: Content of the thought
            
        Returns:
            List of tags with confidence scores
        """
        # This is a placeholder implementation
        # In a real implementation, this would use NLP techniques or call the OpenAI API directly
        import re
        
        # Extract potential tags (words starting with capital letters, hashtags, etc.)
        potential_tags = set()
        
        # Find hashtags
        hashtags = re.findall(r'#(\w+)', thought_content)
        potential_tags.update(hashtags)
        
        # Find capitalized words (potential proper nouns)
        capitalized = re.findall(r'\b([A-Z][a-z]+)\b', thought_content)
        potential_tags.update(capitalized)
        
        # Find common project indicators
        projects = re.findall(r'\b(project|task|goal|objective)s?\b', thought_content, re.IGNORECASE)
        potential_tags.update([p.lower() for p in projects])
        
        # Find emotional words
        emotions = ["happy", "sad", "angry", "excited", "worried", "anxious", "proud", "frustrated"]
        for emotion in emotions:
            if re.search(r'\b' + emotion + r'\b', thought_content, re.IGNORECASE):
                potential_tags.add(emotion.lower())
        
        # Convert to list of dicts with confidence scores
        return [{"name": tag, "confidence": 0.8, "type": "auto"} for tag in potential_tags]
    
    def _extract_tags_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract tags from agent output text.
        
        Args:
            text: Agent output text
            
        Returns:
            List of tags with confidence scores
        """
        import re
        
        tags = []
        
        # Look for tag listings in various formats
        tag_patterns = [
            r'Tag: ([^,]+), Confidence: (0\.\d+)',
            r'- ([^:]+): (0\.\d+)',
            r'"([^"]+)"\s*:\s*(0\.\d+)'
        ]
        
        for pattern in tag_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                tag_name = match[0].strip()
                confidence = float(match[1])
                tags.append({"name": tag_name, "confidence": confidence, "type": "auto"})
        
        # If no structured tags found, extract potential tags
        if not tags:
            # Extract lines that might be tags
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and len(line) < 30:
                    tags.append({"name": line, "confidence": 0.7, "type": "auto"})
        
        return tags
    
    def _find_related_thoughts(self, thought_content: str, existing_thoughts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Find thoughts related to the given thought.
        
        Args:
            thought_content: Content of the thought
            existing_thoughts: List of existing thoughts
            
        Returns:
            List of related thoughts with relationship types and strength scores
        """
        # This is a placeholder implementation
        # In a real implementation, this would use semantic similarity or call the OpenAI API directly
        import re
        
        related = []
        
        # Extract key terms from the thought
        words = re.findall(r'\b\w{4,}\b', thought_content.lower())
        key_terms = set(words)
        
        # Find thoughts with matching terms
        for thought in existing_thoughts:
            thought_id = thought.get("id", "")
            content = thought.get("content", "").lower()
            
            # Count matching terms
            matches = sum(1 for term in key_terms if term in content)
            
            # Calculate similarity score
            if matches > 0:
                similarity = min(matches / len(key_terms), 0.9)  # Cap at 0.9
                
                # Determine relationship type
                relationship = "similar"
                if "follow" in content or "next" in content or "continue" in content:
                    relationship = "continuation"
                elif "disagree" in content or "however" in content or "but" in content:
                    relationship = "contradiction"
                elif "inspire" in content or "based on" in content or "from" in content:
                    relationship = "inspiration"
                
                related.append({
                    "thought_id": thought_id,
                    "relationship": relationship,
                    "strength": similarity
                })
        
        # Sort by strength and return top 5
        related.sort(key=lambda x: x["strength"], reverse=True)
        return related[:5]
    
    def _extract_links_from_text(self, text: str, existing_thoughts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract links from agent output text.
        
        Args:
            text: Agent output text
            existing_thoughts: List of existing thoughts
            
        Returns:
            List of links with relationship types and strength scores
        """
        import re
        
        links = []
        
        # Map thought IDs to indices
        id_to_index = {thought.get("id", ""): i for i, thought in enumerate(existing_thoughts)}
        
        # Look for link listings in various formats
        link_patterns = [
            r'Thought (\d+) \(ID: ([^)]+)\).*?Relationship: ([^,]+), Strength: (0\.\d+)',
            r'- Thought (\d+): ([^,]+), ([^,]+), (0\.\d+)',
            r'"([^"]+)"\s*:\s*\{\s*"relationship"\s*:\s*"([^"]+)"\s*,\s*"strength"\s*:\s*(0\.\d+)'
        ]
        
        for pattern in link_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                thought_id = match[1] if len(match) > 1 else match[0]
                relationship = match[2] if len(match) > 2 else "similar"
                strength = float(match[3]) if len(match) > 3 else 0.7
                
                # Ensure thought_id is valid
                if thought_id in id_to_index:
                    links.append({
                        "thought_id": thought_id,
                        "relationship": relationship,
                        "strength": strength
                    })
        
        return links
    
    def _generate_reflection(self, thought_content: str, related_thoughts: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Generate a reflection based on thought content.
        
        Args:
            thought_content: Content of the thought
            related_thoughts: List of related thoughts for context
            
        Returns:
            Generated reflection
        """
        # This is a placeholder implementation
        # In a real implementation, this would call the OpenAI API directly
        
        # Simple reflection based on content length and keywords
        import re
        
        # Check for question marks
        if "?" in thought_content:
            return "This thought contains questions that might benefit from further exploration or research."
        
        # Check for emotional content
        emotions = ["happy", "sad", "angry", "excited", "worried", "anxious", "proud", "frustrated"]
        found_emotions = [e for e in emotions if re.search(r'\b' + e + r'\b', thought_content, re.IGNORECASE)]
        if found_emotions:
            emotion_str = ", ".join(found_emotions)
            return f"This thought expresses {emotion_str} emotions. Consider how these feelings influence your perspective and decision-making."
        
        # Check for action-oriented content
        if re.search(r'\b(should|must|need to|have to|will)\b', thought_content, re.IGNORECASE):
            return "This thought contains action-oriented language. Consider breaking down these intentions into specific, achievable steps."
        
        # Default reflection
        return "This thought represents an externalization of your internal processing. Consider how it connects to your broader goals and values."
    
    def _summarize_thought(self, thought_content: str) -> str:
        """
        Generate a concise summary of a thought.
        
        Args:
            thought_content: Content of the thought
            
        Returns:
            Generated summary
        """
        # This is a placeholder implementation
        # In a real implementation, this would call the OpenAI API directly
        
        # Simple summary: first sentence or first 100 characters
        import re
        
        # Try to get first sentence
        sentences = re.split(r'(?<=[.!?])\s+', thought_content)
        if sentences:
            first_sentence = sentences[0].strip()
            if len(first_sentence) > 10:  # Ensure it's a meaningful sentence
                return first_sentence
        
        # Fallback to first 100 characters
        if len(thought_content) > 100:
            return thought_content[:97] + "..."
        
        return thought_content
    
    def _extract_actions(self, thought_content: str) -> List[Dict[str, Any]]:
        """
        Extract actionable items from thought content.
        
        Args:
            thought_content: Content of the thought
            
        Returns:
            List of actions with priority and due date
        """
        # This is a placeholder implementation
        # In a real implementation, this would use NLP techniques or call the OpenAI API directly
        import re
        
        actions = []
        
        # Look for common action patterns
        action_patterns = [
            r'(?:need to|should|must|will|going to) ([^.!?]+)[.!?]',
            r'(?:todo|to-do|to do):? ([^.!?]+)[.!?]',
            r'(?:task|action item):? ([^.!?]+)[.!?]'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, thought_content, re.IGNORECASE)
            for match in matches:
                action_text = match.strip()
                
                # Determine priority
                priority = "medium"
                if re.search(r'\b(urgent|important|critical|asap|immediately)\b', action_text, re.IGNORECASE):
                    priority = "high"
                elif re.search(r'\b(later|eventually|sometime|low priority)\b', action_text, re.IGNORECASE):
                    priority = "low"
                
                # Extract due date if present
                due_date = None
                date_match = re.search(r'\b(today|tomorrow|next week|by ([a-zA-Z]+ \d+))\b', action_text, re.IGNORECASE)
                if date_match:
                    due_date = date_match.group(1)
                
                actions.append({
                    "content": action_text,
                    "priority": priority,
                    "due_date": due_date
                })
        
        return actions
    
    def _extract_actions_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract actions from agent output text.
        
        Args:
            text: Agent output text
            
        Returns:
            List of actions with priority and due date
        """
        import re
        
        actions = []
        
        # Look for action listings in various formats
        action_patterns = [
            r'Action: ([^,]+), Priority: ([^,]+), Due Date: ([^\n]+)',
            r'- ([^:]+): Priority: ([^,]+), Due: ([^\n]+)',
            r'- ([^:]+): ([^,]+) priority(?:, due ([^\n]+))?'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                content = match[0].strip()
                priority = match[1].strip().lower() if match[1].strip() else "medium"
                due_date = match[2].strip() if len(match) > 2 and match[2].strip() else None
                
                actions.append({
                    "content": content,
                    "priority": priority,
                    "due_date": due_date
                })
        
        # If no structured actions found, look for bullet points or numbered lists
        if not actions:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('*') or re.match(r'^\d+\.', line):
                    content = re.sub(r'^[-*\d.]+\s*', '', line).strip()
                    if content:
                        priority = "medium"
                        due_date = None
                        
                        # Try to extract priority
                        if "high priority" in content.lower():
                            priority = "high"
                            content = re.sub(r'high priority', '', content, flags=re.IGNORECASE).strip()
                        elif "low priority" in content.lower():
                            priority = "low"
                            content = re.sub(r'low priority', '', content, flags=re.IGNORECASE).strip()
                        
                        # Try to extract due date
                        date_match = re.search(r'\b(today|tomorrow|next week|by ([a-zA-Z]+ \d+))\b', content, re.IGNORECASE)
                        if date_match:
                            due_date = date_match.group(1)
                            content = re.sub(date_match.group(0), '', content).strip()
                        
                        actions.append({
                            "content": content,
                            "priority": priority,
                            "due_date": due_date
                        })
        
        return actions
