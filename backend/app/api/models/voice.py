"""
Voice processing models for VoiceTaskAI
"""
from typing import Optional
from pydantic import BaseModel, Field


class VoiceTranscriptionRequest(BaseModel):
    """Voice transcription request model"""
    audio_file: bytes = Field(..., description="Audio file content")
    filename: str = Field(..., description="Audio file name")


class VoiceTranscriptionResponse(BaseModel):
    """Voice transcription response model"""
    transcription: str = Field(..., description="Transcribed text from audio")
    confidence: Optional[float] = Field(None, description="Transcription confidence score")
    language: Optional[str] = Field(None, description="Detected language")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")


class VoiceProcessingResponse(BaseModel):
    """Complete voice processing response model"""
    transcription: VoiceTranscriptionResponse
    task: Optional[dict] = Field(None, description="Extracted task information")
    success: bool = Field(..., description="Processing success status")
    message: str = Field(..., description="Processing result message")
    errors: Optional[list] = Field(None, description="Any processing errors")
