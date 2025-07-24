"""
Voice processing utilities for VoiceTaskAI
"""
import os
import tempfile
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import whisper
import ffmpeg

from app.config import settings

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)


class VoiceProcessor:
    """Voice processing class using Whisper for transcription"""
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize voice processor with Whisper model
        
        Args:
            model_name: Whisper model to use (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model"""
        try:
            logger.info(f"Loading Whisper model: {self.model_name}")
            self.model = whisper.load_model(self.model_name)
            logger.info(f"✅ Whisper model '{self.model_name}' loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load Whisper model: {e}")
            raise
    
    def convert_audio_format(self, input_path: str, output_path: str) -> bool:
        """
        Convert audio file to WAV format using ffmpeg
        
        Args:
            input_path: Path to input audio file
            output_path: Path for output WAV file
            
        Returns:
            bool: True if conversion successful
        """
        try:
            logger.info(f"Converting audio: {input_path} -> {output_path}")
            
            # Use ffmpeg to convert to WAV format
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(stream, output_path, acodec='pcm_s16le', ar=16000)
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
            logger.info(f"✅ Audio conversion successful")
            return True
            
        except Exception as e:
            logger.error(f"❌ Audio conversion failed: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file using Whisper
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dict containing transcription results
        """
        try:
            logger.info(f"Transcribing audio: {audio_path}")
            
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            # Transcribe using Whisper
            result = self.model.transcribe(audio_path)
            
            logger.info(f"✅ Transcription successful: {result['text'][:50]}...")
            
            return {
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
                "segments": result.get("segments", []),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"❌ Transcription failed: {e}")
            return {
                "text": "",
                "language": "unknown",
                "segments": [],
                "success": False,
                "error": str(e)
            }
    
    def process_audio_file(self, audio_data: bytes, filename: str) -> Dict[str, Any]:
        """
        Process audio file from bytes to transcription
        
        Args:
            audio_data: Raw audio file bytes
            filename: Original filename
            
        Returns:
            Dict containing processing results
        """
        try:
            logger.info(f"Processing audio file: {filename}")
            
            # Create temporary file for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_data)
                temp_input_path = temp_file.name
            
            # Convert to WAV if needed
            temp_output_path = temp_input_path.replace(".wav", "_converted.wav")
            
            if not self.convert_audio_format(temp_input_path, temp_output_path):
                raise Exception("Audio conversion failed")
            
            # Transcribe the converted audio
            transcription_result = self.transcribe_audio(temp_output_path)
            
            # Clean up temporary files
            try:
                os.unlink(temp_input_path)
                os.unlink(temp_output_path)
            except:
                pass
            
            return transcription_result
            
        except Exception as e:
            logger.error(f"❌ Audio processing failed: {e}")
            return {
                "text": "",
                "language": "unknown",
                "segments": [],
                "success": False,
                "error": str(e)
            }


# Global voice processor instance
voice_processor = VoiceProcessor(settings.whisper_model) 