"""
Configuration settings for VoiceTaskAI
"""
import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application settings
    app_name: str = "VoiceTaskAI"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Whisper settings
    whisper_model: str = "base"
    whisper_device: str = "cpu"
    
    # spaCy settings
    spacy_model: str = "en_core_web_sm"
    
    # File storage
    data_dir: str = "./data"
    audio_cache_dir: str = "./data/audio_cache"
    tasks_file: str = "./data/tasks.json"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    # Audio processing
    max_audio_size_mb: int = 50
    supported_audio_formats: str = "wav"
    
    # User management
    predefined_users: str = "Alice,Bob,Charlie,Ali"
    
    # Category management
    predefined_categories: str = "Construction,Inspection,Maintenance"
    
    @property
    def supported_formats_list(self) -> List[str]:
        """Convert supported formats string to list"""
        return [fmt.strip() for fmt in self.supported_audio_formats.split(",")]
    
    @property
    def predefined_users_list(self) -> List[str]:
        """Convert predefined users string to list"""
        return [user.strip() for user in self.predefined_users.split(",")]
    
    @property
    def predefined_categories_list(self) -> List[str]:
        """Convert predefined categories string to list"""
        return [category.strip() for category in self.predefined_categories.split(",")]
    
    @property
    def data_path(self) -> Path:
        """Get data directory path"""
        return Path(self.data_dir)
    
    @property
    def audio_cache_path(self) -> Path:
        """Get audio cache directory path"""
        return Path(self.audio_cache_dir)
    
    @property
    def tasks_file_path(self) -> Path:
        """Get tasks file path"""
        return Path(self.tasks_file)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        settings.data_path,
        settings.audio_cache_path,
        Path(settings.log_file).parent
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True) 