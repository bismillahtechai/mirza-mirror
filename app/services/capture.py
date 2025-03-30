"""
Core capture processing module for Mirza Mirror.
This module handles capturing and processing thoughts from various sources.
"""

import os
import uuid
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Thought, Tag
from app.services.memory_service import MemoryService

class CaptureProcessor:
    """
    Capture processor class that handles capturing and processing thoughts.
    """
    
    def __init__(self):
        """
        Initialize the capture processor.
        """
        self.audio_dir = os.getenv("AUDIO_DIR", "./uploads/audio")
        
        # Create audio directory if it doesn't exist
        os.makedirs(self.audio_dir, exist_ok=True)
    
    def process_text_thought(self, db: Session, content: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a text thought.
        
        Args:
            db: Database session
            content: Thought content
            user_id: User ID
            
        Returns:
            Dict containing the processed thought information
        """
        try:
            # Create thought
            thought = Thought(
                id=str(uuid.uuid4()),
                content=content,
                source="text_note",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                metadata={
                    "user_id": user_id,
                    "source_type": "text_note"
                }
            )
            
            db.add(thought)
            db.commit()
            db.refresh(thought)
            
            # Create memory from thought
            memory_service = MemoryService(user_id)
            memory = memory_service.create_memory_from_thought(db, thought)
            
            return {
                "thought_id": thought.id,
                "content": thought.content,
                "source": thought.source,
                "created_at": thought.created_at,
                "memory_id": memory.id
            }
        except Exception as e:
            db.rollback()
            return {"error": f"Error processing text thought: {str(e)}"}
    
    def process_audio_thought(self, db: Session, audio_file_path: str, transcription: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process an audio thought.
        
        Args:
            db: Database session
            audio_file_path: Path to the audio file
            transcription: Transcription of the audio
            user_id: User ID
            
        Returns:
            Dict containing the processed thought information
        """
        try:
            # Create thought
            thought = Thought(
                id=str(uuid.uuid4()),
                content=transcription,
                source="voice_note",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                audio_file=audio_file_path,
                metadata={
                    "user_id": user_id,
                    "source_type": "voice_note",
                    "audio_file": audio_file_path
                }
            )
            
            db.add(thought)
            db.commit()
            db.refresh(thought)
            
            # Create memory from thought
            memory_service = MemoryService(user_id)
            memory = memory_service.create_memory_from_thought(db, thought)
            
            return {
                "thought_id": thought.id,
                "content": thought.content,
                "source": thought.source,
                "created_at": thought.created_at,
                "audio_file": thought.audio_file,
                "memory_id": memory.id
            }
        except Exception as e:
            db.rollback()
            return {"error": f"Error processing audio thought: {str(e)}"}
    
    def add_tags_to_thought(self, db: Session, thought_id: str, tags: List[str]) -> Dict[str, Any]:
        """
        Add tags to a thought.
        
        Args:
            db: Database session
            thought_id: Thought ID
            tags: List of tag names
            
        Returns:
            Dict containing the updated thought information
        """
        try:
            # Get thought
            thought = db.query(Thought).filter(Thought.id == thought_id).first()
            if not thought:
                return {"error": f"Thought with ID {thought_id} not found"}
            
            # Process tags
            added_tags = []
            for tag_name in tags:
                # Check if tag exists
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                
                # Create tag if it doesn't exist
                if not tag:
                    tag = Tag(
                        id=str(uuid.uuid4()),
                        name=tag_name,
                        type="custom",
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
                
                # Add tag to thought if not already added
                if tag not in thought.tags:
                    thought.tags.append(tag)
                    added_tags.append(tag_name)
            
            db.commit()
            db.refresh(thought)
            
            return {
                "thought_id": thought.id,
                "added_tags": added_tags,
                "all_tags": [tag.name for tag in thought.tags]
            }
        except Exception as e:
            db.rollback()
            return {"error": f"Error adding tags to thought: {str(e)}"}
    
    def search_thoughts(self, db: Session, query: str, limit: int = 10, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for thoughts.
        
        Args:
            db: Database session
            query: Search query
            limit: Maximum number of results
            user_id: User ID
            
        Returns:
            Dict containing the search results
        """
        try:
            # Use memory service to search for relevant memories
            memory_service = MemoryService(user_id)
            memories = memory_service.search_memories(query, limit)
            
            # Get thoughts for the memories
            thoughts = []
            for memory in memories:
                # Extract thought_id from metadata
                thought_id = memory.get("metadata", {}).get("thought_id")
                if thought_id:
                    thought = db.query(Thought).filter(Thought.id == thought_id).first()
                    if thought:
                        thoughts.append({
                            "id": thought.id,
                            "content": thought.content,
                            "source": thought.source,
                            "created_at": thought.created_at,
                            "tags": [tag.name for tag in thought.tags],
                            "relevance": memory.get("score", 0)
                        })
            
            return {
                "query": query,
                "results": thoughts
            }
        except Exception as e:
            return {"error": f"Error searching thoughts: {str(e)}"}
    
    def get_thought_by_id(self, db: Session, thought_id: str) -> Dict[str, Any]:
        """
        Get a thought by ID.
        
        Args:
            db: Database session
            thought_id: Thought ID
            
        Returns:
            Dict containing the thought information
        """
        try:
            thought = db.query(Thought).filter(Thought.id == thought_id).first()
            if not thought:
                return {"error": f"Thought with ID {thought_id} not found"}
            
            return {
                "id": thought.id,
                "content": thought.content,
                "source": thought.source,
                "created_at": thought.created_at,
                "updated_at": thought.updated_at,
                "audio_file": thought.audio_file,
                "document_file": thought.document_file,
                "summary": thought.summary,
                "tags": [tag.name for tag in thought.tags],
                "metadata": thought.metadata
            }
        except Exception as e:
            return {"error": f"Error getting thought: {str(e)}"}
    
    def get_recent_thoughts(self, db: Session, limit: int = 10) -> Dict[str, Any]:
        """
        Get recent thoughts.
        
        Args:
            db: Database session
            limit: Maximum number of results
            
        Returns:
            Dict containing the recent thoughts
        """
        try:
            thoughts = db.query(Thought).order_by(Thought.created_at.desc()).limit(limit).all()
            
            return {
                "thoughts": [
                    {
                        "id": thought.id,
                        "content": thought.content,
                        "source": thought.source,
                        "created_at": thought.created_at,
                        "tags": [tag.name for tag in thought.tags]
                    }
                    for thought in thoughts
                ]
            }
        except Exception as e:
            return {"error": f"Error getting recent thoughts: {str(e)}"}
    
    def get_thoughts_by_tag(self, db: Session, tag_name: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get thoughts by tag.
        
        Args:
            db: Database session
            tag_name: Tag name
            limit: Maximum number of results
            
        Returns:
            Dict containing the thoughts with the specified tag
        """
        try:
            # Get tag
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                return {"error": f"Tag with name {tag_name} not found"}
            
            # Get thoughts with the tag
            thoughts = tag.thoughts[:limit]
            
            return {
                "tag": tag_name,
                "thoughts": [
                    {
                        "id": thought.id,
                        "content": thought.content,
                        "source": thought.source,
                        "created_at": thought.created_at,
                        "tags": [t.name for t in thought.tags]
                    }
                    for thought in thoughts
                ]
            }
        except Exception as e:
            return {"error": f"Error getting thoughts by tag: {str(e)}"}
    
    def delete_thought(self, db: Session, thought_id: str) -> Dict[str, Any]:
        """
        Delete a thought.
        
        Args:
            db: Database session
            thought_id: Thought ID
            
        Returns:
            Dict containing the result of the deletion
        """
        try:
            thought = db.query(Thought).filter(Thought.id == thought_id).first()
            if not thought:
                return {"error": f"Thought with ID {thought_id} not found"}
            
            # Delete the thought
            db.delete(thought)
            db.commit()
            
            return {
                "success": True,
                "message": f"Thought with ID {thought_id} deleted successfully"
            }
        except Exception as e:
            db.rollback()
            return {"error": f"Error deleting thought: {str(e)}"}
