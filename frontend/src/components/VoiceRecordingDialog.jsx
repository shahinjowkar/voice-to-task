import React, { useState, useRef, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  CircularProgress,
  IconButton,
  Paper
} from '@mui/material';
import {
  Mic,
  Stop,
  PlayArrow,
  Delete,
  Send
} from '@mui/icons-material';

const VoiceRecordingDialog = ({ open, onClose, onTaskCreated }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [permissionError, setPermissionError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(null);

  // Function to convert audio blob to WAV format
  const convertToWav = async (audioBlob) => {
    return new Promise((resolve, reject) => {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const fileReader = new FileReader();
      
      fileReader.onload = async (event) => {
        try {
          const arrayBuffer = event.target.result;
          const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
          
          // Create WAV file from audio buffer
          const wavBlob = audioBufferToWav(audioBuffer);
          resolve(wavBlob);
        } catch (error) {
          reject(error);
        }
      };
      
      fileReader.onerror = reject;
      fileReader.readAsArrayBuffer(audioBlob);
    });
  };

  // Function to convert AudioBuffer to WAV blob
  const audioBufferToWav = (buffer) => {
    const length = buffer.length;
    const numberOfChannels = buffer.numberOfChannels;
    const sampleRate = buffer.sampleRate;
    const arrayBuffer = new ArrayBuffer(44 + length * numberOfChannels * 2);
    const view = new DataView(arrayBuffer);
    
    // WAV file header
    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };
    
    writeString(0, 'RIFF');
    view.setUint32(4, 36 + length * numberOfChannels * 2, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, numberOfChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * numberOfChannels * 2, true);
    view.setUint16(32, numberOfChannels * 2, true);
    view.setUint16(34, 16, true);
    writeString(36, 'data');
    view.setUint32(40, length * numberOfChannels * 2, true);
    
    // Write audio data
    let offset = 44;
    for (let i = 0; i < length; i++) {
      for (let channel = 0; channel < numberOfChannels; channel++) {
        const sample = Math.max(-1, Math.min(1, buffer.getChannelData(channel)[i]));
        view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
        offset += 2;
      }
    }
    
    return new Blob([arrayBuffer], { type: 'audio/wav' });
  };

  useEffect(() => {
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  // Reset states when dialog opens/closes
  useEffect(() => {
    if (!open) {
      // Clean up when dialog closes
      if (isRecording) {
        stopRecording();
      }
      // Stop any playing audio
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
      setAudioBlob(null);
      setAudioUrl(null);
      setTranscription('');
      setPermissionError('');
      setIsRecording(false);
      setIsPaused(false);
      setIsPlaying(false);
      audioChunksRef.current = [];
    } else {
      // Reset states when dialog opens
      setPermissionError('');
    }
  }, [open]);

  const startRecording = async () => {
    // Don't start if already recording
    if (isRecording) return;
    
    try {
      // Clear any previous permission errors and reset states
      setPermissionError('');
      setAudioBlob(null);
      setAudioUrl(null);
      setTranscription('');
      audioChunksRef.current = [];
      
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Get supported MIME types for better format control
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') 
        ? 'audio/webm;codecs=opus'
        : MediaRecorder.isTypeSupported('audio/webm') 
        ? 'audio/webm'
        : 'audio/mp4';
      
      mediaRecorderRef.current = new MediaRecorder(stream, { mimeType });
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        // Use the actual MIME type from the MediaRecorder
        const mimeType = mediaRecorderRef.current.mimeType || 'audio/webm';
        const originalBlob = new Blob(audioChunksRef.current, { type: mimeType });
        
        // Convert to WAV format
        try {
          const wavBlob = await convertToWav(originalBlob);
          setAudioBlob(wavBlob);
          const url = URL.createObjectURL(wavBlob);
          setAudioUrl(url);
        } catch (error) {
          console.error('Error converting to WAV:', error);
          // Fallback to original format if conversion fails
          setAudioBlob(originalBlob);
          const url = URL.createObjectURL(originalBlob);
          setAudioUrl(url);
        }
        
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setIsPaused(false);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      
      // Reset recording state on error
      setIsRecording(false);
      setIsPaused(false);
      
      // Handle different types of permission errors
      if (error.name === 'NotAllowedError') {
        setPermissionError('Microphone access denied. Please allow microphone access in your browser settings and try again.');
      } else if (error.name === 'NotFoundError') {
        setPermissionError('No microphone found. Please connect a microphone and try again.');
      } else if (error.name === 'NotReadableError') {
        setPermissionError('Microphone is already in use by another application. Please close other apps using the microphone.');
      } else {
        setPermissionError('Unable to access microphone. Please check your browser settings and try again.');
      }
    }
  };

  const pauseRecording = () => {
    if (mediaRecorderRef.current && isRecording && !isPaused) {
      mediaRecorderRef.current.pause();
      setIsPaused(true);
    } else if (mediaRecorderRef.current && isRecording && isPaused) {
      mediaRecorderRef.current.resume();
      setIsPaused(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsPaused(false);
      // Clear permission error when recording stops successfully
      setPermissionError('');
    }
  };

  const handleRecordButtonClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const playRecording = async () => {
    if (audioRef.current) {
      try {
        // Reset audio to beginning if it has ended
        if (audioRef.current.ended) {
          audioRef.current.currentTime = 0;
        }
        
        await audioRef.current.play();
        setIsPlaying(true);
      } catch (error) {
        console.error('Error playing audio:', error);
        setIsPlaying(false);
      }
    }
  };

  const handleAudioEnded = () => {
    setIsPlaying(false);
  };

  const handleAudioPause = () => {
    setIsPlaying(false);
  };

  const handleAudioPlay = () => {
    setIsPlaying(true);
  };

  const deleteRecording = () => {
    // Stop any playing audio
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);
    setAudioBlob(null);
    setAudioUrl(null);
    setTranscription('');
    setPermissionError('');
    audioChunksRef.current = [];
  };

  const processVoiceToTask = async () => {
    if (!audioBlob) return;

    setIsProcessing(true);
    try {
      const formData = new FormData();
      // Always use WAV format
      formData.append('audio', audioBlob, 'recording.wav');

      const response = await fetch('http://localhost:8000/process-voice', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setTranscription(result.transcription || 'Voice processed successfully');
        
        // If task was created, call the callback
        if (result.task && onTaskCreated) {
          onTaskCreated(result.task);
        }
      } else {
        throw new Error('Failed to process voice');
      }
    } catch (error) {
      console.error('Error processing voice:', error);
      setTranscription('Error processing voice. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const submitRecording = async () => {
    if (!audioBlob) return;

    setIsSubmitting(true);
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.wav');

      const response = await fetch('http://localhost:8000/save-audio', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        
        if (result.success) {
          // Display the task information
          setTranscription(result.transcription);
          
          // Show task details in a more user-friendly way
          const taskInfo = result.task;
          let taskMessage = `Task processed successfully!\n\n`;
          taskMessage += `Transcription: ${result.transcription}\n\n`;
          
          if (taskInfo) {
            taskMessage += `Task Details:\n`;
            if (taskInfo.get('title')) taskMessage += `Title: ${taskInfo.title}\n`;
            if (taskInfo.get('description')) taskMessage += `Description: ${taskInfo.description}\n`;
            if (taskInfo.get('assignee')) taskMessage += `Assignee: ${taskInfo.assignee}\n`;
            if (taskInfo.get('deadline')) taskMessage += `Deadline: ${taskInfo.deadline}\n`;
            if (taskInfo.get('priority')) taskMessage += `Priority: ${taskInfo.priority}\n`;
            if (taskInfo.get('category')) taskMessage += `Category: ${taskInfo.category}\n`;
          }
          
          alert(taskMessage);
        } else {
          alert(`Processing failed: ${result.error || 'Unknown error'}`);
        }
      } else {
        throw new Error('Failed to process audio');
      }
    } catch (error) {
      console.error('Error processing audio:', error);
      alert('Error processing audio. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    if (isRecording) {
      stopRecording();
    }
    setAudioBlob(null);
    setAudioUrl(null);
    setTranscription('');
    setPermissionError('');
    onClose();
  };

  return (
    <Dialog 
      open={open} 
      onClose={handleClose}
      maxWidth="sm"
      fullWidth
    >
      <DialogTitle sx={{ bgcolor: '#181818', color: '#fff' }}>
        Add Task with Voice
      </DialogTitle>
      
      <DialogContent sx={{ bgcolor: '#181818', color: '#fff', pt: 2 }}>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          {!audioBlob ? (
            <Box>
              <Typography variant="body1" color="#bdbdbd" mb={2}>
                Click the microphone to start recording your task
              </Typography>
              <IconButton
                onClick={handleRecordButtonClick}
                sx={{
                  width: 80,
                  height: 80,
                  bgcolor: isRecording ? '#f44336' : '#2196f3',
                  color: '#fff',
                  '&:hover': {
                    bgcolor: isRecording ? '#d32f2f' : '#1976d2',
                  }
                }}
              >
                {isRecording ? <Stop /> : <Mic />}
              </IconButton>
              {isRecording && (
                <Typography variant="body2" color="#f44336" mt={1}>
                  Recording... Click to stop
                </Typography>
              )}
              {permissionError && !isRecording && (
                <Paper sx={{ p: 2, bgcolor: '#f44336', mt: 2, maxWidth: '100%' }}>
                  <Typography variant="body2" color="#fff" sx={{ fontSize: '0.875rem' }}>
                    {permissionError}
                  </Typography>
                </Paper>
              )}
            </Box>
          ) : (
            <Box>
              <Typography variant="body1" color="#bdbdbd" mb={2}>
                Recording complete! Listen or process your voice
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', mb: 2 }}>
                <IconButton
                  onClick={playRecording}
                  disabled={isPlaying}
                  sx={{
                    bgcolor: '#4caf50',
                    color: '#fff',
                    '&:hover': { bgcolor: '#388e3c' },
                    '&:disabled': { bgcolor: '#666' }
                  }}
                >
                  <PlayArrow />
                </IconButton>
                
                <IconButton
                  onClick={deleteRecording}
                  sx={{
                    bgcolor: '#f44336',
                    color: '#fff',
                    '&:hover': { bgcolor: '#d32f2f' }
                  }}
                >
                  <Delete />
                </IconButton>
              </Box>

              {audioUrl && (
                <audio
                  ref={audioRef}
                  src={audioUrl}
                  onEnded={handleAudioEnded}
                  onPause={handleAudioPause}
                  onPlay={handleAudioPlay}
                  style={{ display: 'none' }}
                />
              )}

              {transcription && (
                <Paper sx={{ p: 2, bgcolor: '#333', mt: 2 }}>
                  <Typography variant="body2" color="#fff">
                    <strong>Transcription:</strong> {transcription}
                  </Typography>
                </Paper>
              )}
            </Box>
          )}
        </Box>
      </DialogContent>

      <DialogActions sx={{ bgcolor: '#181818', color: '#fff' }}>
        <Button onClick={handleClose} color="inherit">
          Cancel
        </Button>
        {audioBlob && (
          <>
            <Button
              onClick={submitRecording}
              disabled={isSubmitting}
              variant="outlined"
              startIcon={isSubmitting ? <CircularProgress size={16} /> : <Send />}
              sx={{ 
                color: '#4caf50', 
                borderColor: '#4caf50',
                '&:hover': { 
                  borderColor: '#388e3c',
                  bgcolor: 'rgba(76, 175, 80, 0.1)'
                }
              }}
            >
              {isSubmitting ? 'Saving...' : 'Save Audio'}
            </Button>
            <Button
              onClick={processVoiceToTask}
              disabled={isProcessing}
              variant="contained"
              startIcon={isProcessing ? <CircularProgress size={16} /> : <Send />}
              sx={{ bgcolor: '#2196f3', '&:hover': { bgcolor: '#1976d2' } }}
            >
              {isProcessing ? 'Processing...' : 'Create Task'}
            </Button>
          </>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default VoiceRecordingDialog; 