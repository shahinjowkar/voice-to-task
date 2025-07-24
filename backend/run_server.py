#!/usr/bin/env python3
"""
Development server runner for VoiceTaskAI API
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("Starting VoiceTaskAI API server...")
    print("API will be available at: http://localhost:8000")
    print("API documentation will be available at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    ) 