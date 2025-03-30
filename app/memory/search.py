"""
Memory service for Mirza Mirror using mem0 integration.
This service provides higher-level functions for memory management.
"""

import uuid
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from app.memory import MemoryManager
from app.models import Memory, Thought
from app.database import get_db

class MemoryService:
    """
    Service class that provides memory management functionality.
    Integrates mem0 with the database models.
    """
    
    def __init__(self, user_id: str = None):
        """
        Initialize the memory service.
        
        Args:
            user_id: The user identifier for memory context
        """
        self.memory_manager = MemoryManager(user_id)
        self.user_id = self.memory_manager.user_id
    
    def create_memory_from_thought(self, db: Session, thought: Thought) -> Memory:
        """
        Create a memory from a thought and store it in both mem0 and the database.
        
        Args:
            db: Database session
            thought: Thought object to create memory from
            
        Returns:
            Memory object
        """
        # Create memory in mem0
        memory_result = self.memory_manager.add_memory(
            content=thought.content,
            metadata={
                "source": thought.source,
                "created_at": thought.created_at.isoformat(),
                "thought_id": thought.id
            }
        )
        
        # Create memory in database
        db_memory = Memory(
            id=memory_result.get("id", str(uuid.uuid4())),
            user_id=self.user_id,
            thought_id=thought.id,
            memory=thought.content,
            created_at=thought.created_at,
            memory_type="user",
            metadata={
                "source": thought.source,
                "mem0_id": memory_result.get("id")
            }
        )
        
        db.add(db_memory)
        db.commit()
        db.refresh(db_memory)
        
        return db_memory
    
    def search_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant memories based on a query.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            List of relevant memories
        """
        return self.memory_manager.search_memories(query, limit)
    
    def get_memories_for_thought(self, db: Session, thought_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get relevant memories for a specific thought.
        
        Args:
            db: Database session
            thought_id: ID of the thought
            limit: Maximum number of results to return
            
        Returns:
            List of relevant memories
        """
        # Get the thought from the database
        thought = db.query(Thought).filter(Thought.id == thought_id).first()
        if not thought:
            return []
        
        # Search for relevant memories
        return self.memory_manager.search_memories(thought.content, limit)
    
    def generate_reflection(self, context: str, limit: int = 5) -> Dict[str, Any]:
        """
        Generate a reflection based on relevant memories.
        
        Args:
            context: The context for the reflection
            limit: Maximum number of memories to consider
            
        Returns:
            Dict containing the reflection information
        """
        return self.memory_manager.generate_reflection(context, limit)
    
    def create_memory_from_conversation(self, db: Session, conversation_id: str) -> List[Memory]:
        """
        Create memories from an imported conversation.
        
        Args:
            db: Database session
            conversation_id: ID of the imported conversation
            
        Returns:
            List of created Memory objects
        """
        from app.models import ImportedConversation, ConversationThought
        
        # Get the conversation and associated thoughts
        conversation = db.query(ImportedConversation).filter(
            ImportedConversation.id == conversation_id
        ).first()
        
        if not conversation:
            return []
        
        conversation_thoughts = db.query(ConversationThought).filter(
            ConversationThought.conversation_id == conversation_id
        ).all()
        
        created_memories = []
        
        # Create memories for each thought in the conversation
        for ct in conversation_thoughts:
            thought = db.query(Thought).filter(Thought.id == ct.thought_id).first()
            if thought:
                memory = self.create_memory_from_thought(db, thought)
                created_memories.append(memory)
        
        return created_memories
    
    def delete_memory(self, db: Session, memory_id: str) -> bool:
        """
        Delete a memory from both mem0 and the database.
        
        Args:
            db: Database session
            memory_id: ID of the memory to delete
            
        Returns:
            True if successful, False otherwise
        """
        # Delete from mem0
        mem0_success = self.memory_manager.delete_memory(memory_id)
        
        # Delete from database
        db_memory = db.query(Memory).filter(Memory.id == memory_id).first()
        if db_memory:
            db.delete(db_memory)
            db.commit()
            return True
        
        return mem0_success
