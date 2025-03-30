"""
Transcription service using Whisper for Mirza Mirror.
"""

import os
import tempfile
from typing import Dict, Any, Optional
import whisper
from app.utils.logger import log_info, log_error

class TranscriptionService:
    """
    Transcription service using OpenAI's Whisper model.
    """
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize the transcription service.
        
        Args:
            model_name: Whisper model name (tiny, base, small, medium, large)
        """
        try:
            self.model = whisper.load_model(model_name)
            log_info(f"Loaded Whisper model: {model_name}")
        except Exception as e:
            log_error(f"Error loading Whisper model: {str(e)}")
            raise
    
    def transcribe_audio(self, audio_file_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio file using Whisper.
        
        Args:
            audio_file_path: Path to the audio file
            language: Language code (optional)
            
        Returns:
            Dict containing the transcription result
        """
        try:
            log_info(f"Transcribing audio file: {audio_file_path}")
            
            # Set transcription options
            options = {}
            if language:
                options["language"] = language
            
            # Transcribe audio
            result = self.model.transcribe(audio_file_path, **options)
            
            log_info(f"Transcription completed successfully")
            return result
        except Exception as e:
            log_error(f"Error transcribing audio: {str(e)}")
            return {"error": str(e)}
    
    def transcribe_audio_segments(self, audio_file_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio file with segment timestamps using Whisper.
        
        Args:
            audio_file_path: Path to the audio file
            language: Language code (optional)
            
        Returns:
            Dict containing the transcription result with segments
        """
        try:
            log_info(f"Transcribing audio file with segments: {audio_file_path}")
            
            # Set transcription options
            options = {"word_timestamps": True}
            if language:
                options["language"] = language
            
            # Transcribe audio
            result = self.model.transcribe(audio_file_path, **options)
            
            log_info(f"Segmented transcription completed successfully")
            return result
        except Exception as e:
            log_error(f"Error transcribing audio segments: {str(e)}")
            return {"error": str(e)}
