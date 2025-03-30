"""
Memory module for Mirza Mirror using mem0 integration.
This module handles the memory layer for the thought externalization system.
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from mem0 import Memory as Mem0Memory

# Load environment variables
load_dotenv()

class MemoryManager:
    """
    Memory manager class that integrates mem0 for intelligent memory management.
    Provides methods for adding, searching, and retrieving memories.
    """
    
    def __init__(self, user_id: str = None):
        """
        Initialize the memory manager with mem0.
        
        Args:
            user_id: The user identifier for memory context
        """
        self.memory = Mem0Memory()
        self.user_id = user_id or os.getenv("MEM0_USER_ID", "default_user")
    
    def add_memory(self, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Add a new memory to mem0.
        
        Args:
            content: The content of the memory
            metadata: Additional metadata for the memory
            
        Returns:
            Dict containing the memory information
        """
        # Create a message format that mem0 can process
        messages = [
            {"role": "user", "content": content}
        ]
        
        # Add the memory to mem0
        memory_result = self.memory.add(messages, user_id=self.user_id, metadata=metadata or {})
        
        return memory_result
    
    def search_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant memories based on a query.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            List of relevant memories
        """
        # Search for memories in mem0
        search_results = self.memory.search(
            query=query,
            user_id=self.user_id,
            limit=limit
        )
        
        return search_results.get("results", [])
    
    def get_memories_by_tag(self, tag: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get memories associated with a specific tag.
        
        Args:
            tag: The tag to search for
            limit: Maximum number of results to return
            
        Returns:
            List of memories with the specified tag
        """
        # Search for memories with the specified tag
        tag_query = f"tag:{tag}"
        search_results = self.memory.search(
            query=tag_query,
            user_id=self.user_id,
            limit=limit
        )
        
        return search_results.get("results", [])
    
    def get_memories_by_date_range(self, start_date: str, end_date: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get memories within a specific date range.
        
        Args:
            start_date: Start date in ISO format (YYYY-MM-DD)
            end_date: End date in ISO format (YYYY-MM-DD)
            limit: Maximum number of results to return
            
        Returns:
            List of memories within the date range
        """
        # Search for memories within the date range
        date_query = f"date>={start_date} AND date<={end_date}"
        search_results = self.memory.search(
            query=date_query,
            user_id=self.user_id,
            limit=limit
        )
        
        return search_results.get("results", [])
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a specific memory.
        
        Args:
            memory_id: The ID of the memory to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.memory.delete(memory_id, user_id=self.user_id)
            return True
        except Exception:
            return False
    
    def generate_reflection(self, context: str, limit: int = 5) -> Dict[str, Any]:
        """
        Generate a reflection based on relevant memories.
        
        Args:
            context: The context for the reflection
            limit: Maximum number of memories to consider
            
        Returns:
            Dict containing the reflection information
        """
        # Get relevant memories
        relevant_memories = self.search_memories(context, limit=limit)
        
        # Format memories for reflection
        memories_str = "\n".join([f"- {memory['memory']}" for memory in relevant_memories])
        
        # Create a message format for reflection
        reflection_prompt = f"Based on these memories:\n{memories_str}\n\nGenerate a reflection about {context}"
        messages = [
            {"role": "system", "content": "You are a reflective AI that helps users understand patterns in their thoughts."},
            {"role": "user", "content": reflection_prompt}
        ]
        
        # Use mem0 to generate the reflection
        reflection_result = self.memory.reflect(messages, user_id=self.user_id)
        
        return {
            "reflection": reflection_result.get("reflection", ""),
            "based_on": relevant_memories
        }
