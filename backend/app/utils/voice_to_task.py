"""
Voice-to-task pipeline: Connects Whisper transcription and spaCy task parsing
"""
from typing import Dict, Any
from app.utils.voice_processor import voice_processor
from app.utils.task_parser import task_parser


def voice_to_task(audio_bytes: bytes, filename: str) -> Dict[str, Any]:
    """
    Full pipeline: audio file → Whisper transcription → spaCy task extraction
    Args:
        audio_bytes: Raw audio file bytes
        filename: Name of the audio file
    Returns:
        Dict with transcription, task info, and success status
    """
    # Step 1: Transcribe audio
    transcription_result = voice_processor.process_audio_file(audio_bytes, filename)
    
    if not transcription_result.get('success'):
        return {
            'success': False,
            'error': transcription_result.get('error', 'Transcription failed'),
            'transcription': transcription_result.get('text', ''),
            'task': None
        }
    
    # Step 2: Parse task from transcription
    text = transcription_result['text']
    task_info = task_parser.parse_task_command(text)
    
    return {
        'success': task_info.get('success', False),
        'transcription': text,
        'task': task_info,
        'error': task_info.get('errors', [])
    } 