#!/usr/bin/env python3
"""
Simple script to test Whisper transcription
"""
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_transcription(audio_file_path):
    """Test transcription with a given audio file"""
    try:
        from app.utils.voice_processor import VoiceProcessor
        
        print(f"🎙️ Testing transcription with: {audio_file_path}")
        print("=" * 50)
        
        # Load the voice processor
        print("📦 Loading Whisper model...")
        processor = VoiceProcessor('base')
        print("✅ Whisper model loaded!")
        
        # Read the audio file
        print(f"📁 Reading audio file: {audio_file_path}")
        with open(audio_file_path, 'rb') as f:
            audio_bytes = f.read()
        print(f"✅ Audio file read ({len(audio_bytes)} bytes)")
        
        # Process the audio
        print("🔄 Processing audio with Whisper...")
        result = processor.process_audio_file(audio_bytes, os.path.basename(audio_file_path))
        
        # Display results
        print("\n" + "=" * 50)
        print("📝 TRANSCRIPTION RESULTS:")
        print("=" * 50)
        
        if result['success']:
            print(f"✅ SUCCESS!")
            print(f"📄 Transcribed Text: '{result['text']}'")
            print(f"🌍 Language: {result['language']}")
            print(f"⏱️  Segments: {len(result['segments'])}")
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
        
        return result['success']
        
    except FileNotFoundError:
        print(f"❌ Error: Audio file not found: {audio_file_path}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🎙️ VoiceTaskAI - Whisper Transcription Test")
    print("=" * 50)
    
    # Check if audio file is provided as argument
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        # Look for common audio files in current directory
        audio_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.webm']
        audio_files = []
        
        for ext in audio_extensions:
            audio_files.extend(Path('.').glob(f'*{ext}'))
        
        if audio_files:
            audio_file = str(audio_files[0])
            print(f"🎵 Found audio file: {audio_file}")
        else:
            print("❌ No audio file found!")
            print("\nUsage:")
            print("  python test_transcription.py <audio_file>")
            print("\nOr place an audio file (.wav, .mp3, .m4a, .flac, .webm) in the current directory.")
            return False
    
    # Test transcription
    success = test_transcription(audio_file)
    
    if success:
        print("\n🎉 Transcription test completed successfully!")
        print("✅ Whisper integration is working correctly!")
    else:
        print("\n❌ Transcription test failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 