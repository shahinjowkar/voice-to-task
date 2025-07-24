from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from datetime import datetime
import shutil
from app.utils.voice_to_task import voice_to_task
from app.storage.task_storage import task_storage, categories_storage
from fastapi.responses import JSONResponse

app = FastAPI(
    title="VoiceTaskAI API",
    description="Voice-Driven Task Assignment System API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello_world():
    """Hello world endpoint"""
    return {"message": "Hello World from VoiceTaskAI!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "VoiceTaskAI API"}

@app.post("/process-voice")
async def process_voice(audio: UploadFile = File(...)):
    """Process voice recording and convert to task"""
    try:
        # Validate file type
        if not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read the audio file content
        content = await audio.read()
        
        # Generate filename for processing
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.wav"
        
        # Process through voice-to-task pipeline
        result = voice_to_task(content, filename)
        
        if not result.get('success'):
            return {
                "success": False,
                "transcription": result.get('transcription', ''),
                "task": None,
                "message": "Failed to process voice",
                "error": result.get('error', 'Unknown error')
            }
        
        # Save the processed audio file to the backend
        audio_cache_dir = "data/audio_cache"
        os.makedirs(audio_cache_dir, exist_ok=True)
        file_path = os.path.join(audio_cache_dir, filename)
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Save the processed task data to storage
        task_data = result.get('task', {})
        transcription = result.get('transcription', '')
        
        # Create processing metadata
        processing_metadata = {
            "audio_file_path": file_path,
            "audio_file_size": len(content),
            "processing_timestamp": datetime.now().isoformat(),
            "pipeline_version": "1.0"
        }
        
        # Save to task storage
        saved_task_path = task_storage.save_processed_task(
            audio_filename=filename,
            transcription=transcription,
            task_data=task_data,
            processing_metadata=processing_metadata
        )

        # Add the task to the correct category in categories.json
        if task_data and task_data.get('category'):
            # Map category name to ID
            category_name = task_data['category']
            categories = categories_storage.load_categories()
            category_id = None
            for cat in categories:
                if cat['title'].lower() == str(category_name).lower() or str(cat['id']) == str(category_name):
                    category_id = cat['id']
                    break
            if category_id:
                category_task = {
                    'title': task_data.get('title'),
                    'assignee': task_data.get('assignee') or task_data.get('name'),
                    'deadline': task_data.get('deadline'),
                    'description': task_data.get('description', ''),
                }
                categories_storage.add_task_to_category(category_id, category_task)
        
        # Return the task JSON if processing was successful
        return {
            "success": True,
            "transcription": transcription,
            "task": task_data,
            "message": "Voice processed successfully",
            "filename": filename,
            "audio_file_path": file_path,
            "task_storage_path": saved_task_path
        }
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing voice: {str(e)}")

@app.post("/save-audio")
async def save_audio(audio: UploadFile = File(...)):
    """Process audio file through voice-to-task pipeline and return task JSON"""
    try:
        # Validate file type
        if not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read the audio file content
        content = await audio.read()
        
        # Generate filename for processing
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.wav"
        
        # Process through voice-to-task pipeline
        result = voice_to_task(content, filename)
        
        if not result.get('success'):
            return {
                "success": False,
                "message": "Failed to process audio",
                "error": result.get('error', 'Unknown error'),
                "transcription": result.get('transcription', ''),
                "task": None
            }
        
        # Save the processed audio file to the backend
        audio_cache_dir = "data/audio_cache"
        os.makedirs(audio_cache_dir, exist_ok=True)
        file_path = os.path.join(audio_cache_dir, filename)
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Save the processed task data to storage
        task_data = result.get('task', {})
        transcription = result.get('transcription', '')
        
        # Create processing metadata
        processing_metadata = {
            "audio_file_path": file_path,
            "audio_file_size": len(content),
            "processing_timestamp": datetime.now().isoformat(),
            "pipeline_version": "1.0"
        }
        
        # Save to task storage
        saved_task_path = task_storage.save_processed_task(
            audio_filename=filename,
            transcription=transcription,
            task_data=task_data,
            processing_metadata=processing_metadata
        )
        
        # Return the task JSON if processing was successful
        return {
            "success": True,
            "message": "Audio processed successfully",
            "transcription": transcription,
            "task": task_data,
            "filename": filename,
            "audio_file_path": file_path,
            "task_storage_path": saved_task_path,
            "file_size": len(content)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@app.get("/tasks")
async def get_all_tasks():
    """Retrieve all processed tasks"""
    try:
        tasks = task_storage.get_all_tasks()
        return {
            "success": True,
            "tasks": tasks,
            "count": len(tasks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tasks: {str(e)}")

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Retrieve a specific task by ID"""
    try:
        task = task_storage.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {
            "success": True,
            "task": task
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task: {str(e)}")

@app.get("/categories")
async def get_categories():
    """Return all categories and their tasks"""
    try:
        categories = categories_storage.load_categories()
        return JSONResponse(content=categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading categories: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 