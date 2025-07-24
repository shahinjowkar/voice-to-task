#!/bin/bash

# VoiceTaskAI Demo Setup Script
# Quick setup for functionality demo

echo "🎙️  VoiceTaskAI Demo Setup"
echo "=========================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg not found. Please install FFmpeg:"
    echo "   macOS: brew install ffmpeg"
    echo "   Ubuntu: sudo apt install ffmpeg"
    exit 1
fi

echo "✅ Dependencies check passed"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install
echo "🔧 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Download spaCy model
echo "🧠 Installing spaCy model..."
python -m spacy download en_core_web_sm

# Create .env
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp env.example .env
fi

echo ""
echo "🎉 Demo setup complete!"
echo ""
echo "To start the demo:"
echo "1. source venv/bin/activate"
echo "2. python -m app.main"
echo "3. Open http://localhost:8000/docs" 