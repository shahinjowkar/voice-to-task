#!/usr/bin/env python3
"""
Test script for the full voice-to-task pipeline
"""
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_voice_to_task(audio_file_path):
    try:
        from app.utils.voice_to_task import voice_to_task
        print(f"🎙️ Testing voice-to-task pipeline with: {audio_file_path}")
        print("=" * 50)
        with open(audio_file_path, 'rb') as f:
            audio_bytes = f.read()
        result = voice_to_task(audio_bytes, Path(audio_file_path).name)
        print("\n📝 Pipeline Output:")
        print("=" * 50)
        print(f"Transcription: {result['transcription']}")
        print(f"Task Extraction: {result['task']}")
        print(f"Success: {result['success']}")
        if result['error']:
            print(f"Errors: {result['error']}")
        return result['success']
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🎙️ VoiceTaskAI - Voice-to-Task Pipeline Test")
    print("=" * 50)
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        # Try to find a .wav file in the current directory
        audio_files = list(Path('.').glob('*.wav'))
        if not audio_files:
            print("❌ No .wav file found!")
            return False
        audio_file = str(audio_files[0])
        print(f"🎵 Found audio file: {audio_file}")
    success = test_voice_to_task(audio_file)
    if success:
        print("\n🎉 Voice-to-task pipeline test completed successfully!")
    else:
        print("\n❌ Voice-to-task pipeline test failed!")
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1) 