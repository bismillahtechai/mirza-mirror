"""
Import functionality for AI assistant conversations in Mirza Mirror.
This module handles importing conversations from various AI assistants.
"""

import os
import json
import uuid
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import ImportedConversation, ConversationThought, Thought

class ConversationImporter:
    """
    Conversation importer class that handles importing conversations from various AI assistants.
    """
    
    def __init__(self):
        """
        Initialize the conversation importer.
        """
        self.import_dir = os.getenv("IMPORT_DIR", "./imports")
        
        # Create import directory if it doesn't exist
        os.makedirs(self.import_dir, exist_ok=True)
    
    def import_conversation(self, db: Session, file_path: str, source: str, format: str) -> Dict[str, Any]:
        """
        Import a conversation from a file.
        
        Args:
            db: Database session
            file_path: Path to the conversation file
            source: Source of the conversation (chatgpt, claude, gemini)
            format: Format of the conversation (markdown, json)
            
        Returns:
            Dict containing the imported conversation information
        """
        try:
            # Parse the conversation based on format
            if format.lower() == "markdown":
                conversation_data = self._parse_markdown_conversation(file_path, source)
            elif format.lower() == "json":
                conversation_data = self._parse_json_conversation(file_path, source)
            else:
                return {"error": f"Unsupported format: {format}"}
            
            # Create imported conversation record
            imported_conversation = ImportedConversation(
                id=str(uuid.uuid4()),
                source=source,
                format=format,
                original_file=file_path,
                imported_at=datetime.utcnow(),
                metadata=conversation_data.get("metadata", {})
            )
            
            db.add(imported_conversation)
            db.commit()
            db.refresh(imported_conversation)
            
            # Create thoughts and conversation thoughts
            conversation_thoughts = []
            for i, message in enumerate(conversation_data.get("messages", [])):
                # Create thought
                thought = Thought(
                    id=str(uuid.uuid4()),
                    content=message.get("content", ""),
                    source=f"import_{source}",
                    created_at=message.get("timestamp", datetime.utcnow()),
                    metadata={
                        "role": message.get("role", "unknown"),
                        "source": source,
                        "format": format,
                        "conversation_id": imported_conversation.id
                    }
                )
                
                db.add(thought)
                db.commit()
                db.refresh(thought)
                
                # Create conversation thought
                conversation_thought = ConversationThought(
                    conversation_id=imported_conversation.id,
                    thought_id=thought.id,
                    segment_index=i,
                    role=message.get("role", "unknown")
                )
                
                db.add(conversation_thought)
                conversation_thoughts.append(conversation_thought)
            
            db.commit()
            
            return {
                "conversation_id": imported_conversation.id,
                "source": source,
                "format": format,
                "message_count": len(conversation_data.get("messages", [])),
                "thoughts": [ct.thought_id for ct in conversation_thoughts]
            }
        except Exception as e:
            db.rollback()
            return {"error": f"Error importing conversation: {str(e)}"}
    
    def _parse_markdown_conversation(self, file_path: str, source: str) -> Dict[str, Any]:
        """
        Parse a markdown conversation file.
        
        Args:
            file_path: Path to the markdown file
            source: Source of the conversation
            
        Returns:
            Dict containing the parsed conversation data
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        messages = []
        metadata = {"source": source, "format": "markdown"}
        
        if source.lower() == "chatgpt":
            # Parse ChatGPT markdown format
            # Format: #### You: ... #### ChatGPT: ...
            user_pattern = r"#{1,6}\s*You:\s*(.*?)(?=#{1,6}\s*ChatGPT:|$)"
            assistant_pattern = r"#{1,6}\s*ChatGPT:\s*(.*?)(?=#{1,6}\s*You:|$)"
            
            user_messages = re.findall(user_pattern, content, re.DOTALL)
            assistant_messages = re.findall(assistant_pattern, content, re.DOTALL)
            
            # Interleave messages (user first, then assistant)
            for i in range(max(len(user_messages), len(assistant_messages))):
                if i < len(user_messages):
                    messages.append({
                        "role": "user",
                        "content": user_messages[i].strip(),
                        "timestamp": datetime.utcnow()
                    })
                
                if i < len(assistant_messages):
                    messages.append({
                        "role": "assistant",
                        "content": assistant_messages[i].strip(),
                        "timestamp": datetime.utcnow()
                    })
        
        elif source.lower() == "claude":
            # Parse Claude markdown format
            # Format: Human: ... Assistant: ...
            user_pattern = r"Human:\s*(.*?)(?=\nAssistant:|\Z)"
            assistant_pattern = r"Assistant:\s*(.*?)(?=\nHuman:|\Z)"
            
            user_messages = re.findall(user_pattern, content, re.DOTALL)
            assistant_messages = re.findall(assistant_pattern, content, re.DOTALL)
            
            # Interleave messages (user first, then assistant)
            for i in range(max(len(user_messages), len(assistant_messages))):
                if i < len(user_messages):
                    messages.append({
                        "role": "user",
                        "content": user_messages[i].strip(),
                        "timestamp": datetime.utcnow()
                    })
                
                if i < len(assistant_messages):
                    messages.append({
                        "role": "assistant",
                        "content": assistant_messages[i].strip(),
                        "timestamp": datetime.utcnow()
                    })
        
        elif source.lower() == "gemini":
            # Parse Gemini markdown format
            # Format: User: ... Model: ...
            user_pattern = r"User:\s*(.*?)(?=\nModel:|\Z)"
            assistant_pattern = r"Model:\s*(.*?)(?=\nUser:|\Z)"
            
            user_messages = re.findall(user_pattern, content, re.DOTALL)
            assistant_messages = re.findall(assistant_pattern, content, re.DOTALL)
            
            # Interleave messages (user first, then assistant)
            for i in range(max(len(user_messages), len(assistant_messages))):
                if i < len(user_messages):
                    messages.append({
                        "role": "user",
                        "content": user_messages[i].strip(),
                        "timestamp": datetime.utcnow()
                    })
                
                if i < len(assistant_messages):
                    messages.append({
                        "role": "assistant",
                        "content": assistant_messages[i].strip(),
                        "timestamp": datetime.utcnow()
                    })
        
        return {
            "messages": messages,
            "metadata": metadata
        }
    
    def _parse_json_conversation(self, file_path: str, source: str) -> Dict[str, Any]:
        """
        Parse a JSON conversation file.
        
        Args:
            file_path: Path to the JSON file
            source: Source of the conversation
            
        Returns:
            Dict containing the parsed conversation data
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        messages = []
        metadata = {"source": source, "format": "json"}
        
        if source.lower() == "chatgpt":
            # Parse ChatGPT JSON format
            if "mapping" in data:
                # ChatGPT conversation export format
                for node_id, node in data.get("mapping", {}).items():
                    if node.get("message") and node.get("message", {}).get("content", {}).get("parts"):
                        message = {
                            "role": node.get("message", {}).get("author", {}).get("role", "unknown"),
                            "content": "\n".join(node.get("message", {}).get("content", {}).get("parts", [])),
                            "timestamp": datetime.fromtimestamp(node.get("message", {}).get("create_time", 0)) if node.get("message", {}).get("create_time") else datetime.utcnow()
                        }
                        messages.append(message)
            elif isinstance(data, list):
                # Simple message list format
                for msg in data:
                    message = {
                        "role": msg.get("role", "unknown"),
                        "content": msg.get("content", ""),
                        "timestamp": datetime.fromisoformat(msg.get("timestamp")) if msg.get("timestamp") else datetime.utcnow()
                    }
                    messages.append(message)
        
        elif source.lower() == "claude":
            # Parse Claude JSON format
            if "conversations" in data:
                # Claude conversation export format
                for conv in data.get("conversations", []):
                    for msg in conv.get("messages", []):
                        message = {
                            "role": "user" if msg.get("type") == "human" else "assistant",
                            "content": msg.get("text", ""),
                            "timestamp": datetime.fromisoformat(msg.get("timestamp")) if msg.get("timestamp") else datetime.utcnow()
                        }
                        messages.append(message)
            elif isinstance(data, list):
                # Simple message list format
                for msg in data:
                    message = {
                        "role": "user" if msg.get("type") == "human" else "assistant",
                        "content": msg.get("text", ""),
                        "timestamp": datetime.fromisoformat(msg.get("timestamp")) if msg.get("timestamp") else datetime.utcnow()
                    }
                    messages.append(message)
        
        elif source.lower() == "gemini":
            # Parse Gemini JSON format
            if "messages" in data:
                # Gemini conversation export format
                for msg in data.get("messages", []):
                    message = {
                        "role": msg.get("role", "unknown"),
                        "content": msg.get("parts", [{}])[0].get("text", ""),
                        "timestamp": datetime.fromisoformat(msg.get("timestamp")) if msg.get("timestamp") else datetime.utcnow()
                    }
                    messages.append(message)
            elif isinstance(data, list):
                # Simple message list format
                for msg in data:
                    message = {
                        "role": msg.get("role", "unknown"),
                        "content": msg.get("content", ""),
                        "timestamp": datetime.fromisoformat(msg.get("timestamp")) if msg.get("timestamp") else datetime.utcnow()
                    }
                    messages.append(message)
        
        return {
            "messages": messages,
            "metadata": metadata
        }
    
    def get_supported_sources(self) -> List[str]:
        """
        Get a list of supported conversation sources.
        
        Returns:
            List of supported sources
        """
        return ["chatgpt", "claude", "gemini"]
    
    def get_supported_formats(self) -> List[str]:
        """
        Get a list of supported conversation formats.
        
        Returns:
            List of supported formats
        """
        return ["markdown", "json"]
