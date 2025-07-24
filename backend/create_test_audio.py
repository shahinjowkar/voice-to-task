#!/usr/bin/env python3
"""
Create a test audio file for Whisper testing
"""
import numpy as np
import wave

def create_test_audio():
    """Create a simple test audio file"""
    print("🎵 Creating test audio file...")
    
    # Audio parameters
    sample_rate = 16000  # 16kHz
    duration = 3  # 3 seconds
    frequency = 440  # 440Hz (A note)
    
    # Generate sine wave
    t = np.linspace(0, duration, sample_rate * duration)
    samples = np.sin(2 * np.pi * frequency * t).astype(np.float32)
    
    # Create WAV file
    with wave.open('test_audio.wav', 'wb') as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes((samples * 32767).astype(np.int16).tobytes())
    
    print("✅ Created test_audio.wav")
    print(f"   Duration: {duration} seconds")
    print(f"   Frequency: {frequency}Hz")
    print(f"   Sample rate: {sample_rate}Hz")
    print(f"   Format: 16-bit mono WAV")

if __name__ == "__main__":
    create_test_audio() 