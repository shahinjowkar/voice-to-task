"""
Task storage utilities for VoiceTaskAI
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class TaskStorage:
    """Storage class for processed task data"""
    
    def __init__(self, storage_dir: str = "data/processed_tasks"):
        """
        Initialize task storage
        
        Args:
            storage_dir: Directory to store processed tasks
        """
        self.storage_dir = storage_dir
        self._ensure_storage_dir()
    
    def _ensure_storage_dir(self):
        """Create storage directory if it doesn't exist"""
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def save_processed_task(self, 
                          audio_filename: str, 
                          transcription: str, 
                          task_data: Dict[str, Any],
                          processing_metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save processed task data to storage
        
        Args:
            audio_filename: Name of the original audio file
            transcription: Whisper transcription text
            task_data: Extracted task information
            processing_metadata: Additional processing metadata
            
        Returns:
            str: Path to the saved task file
        """
        # Generate task ID and filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_id = f"task_{timestamp}"
        task_filename = f"{task_id}.json"
        task_path = os.path.join(self.storage_dir, task_filename)
        
        # Create task record
        task_record = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "audio_filename": audio_filename,
            "transcription": transcription,
            "task_data": task_data,
            "processing_metadata": processing_metadata or {},
            "status": "processed"
        }
        
        # Save to JSON file
        with open(task_path, 'w', encoding='utf-8') as f:
            json.dump(task_record, f, indent=2, ensure_ascii=False)
        
        return task_path
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific task by ID
        
        Args:
            task_id: Task ID to retrieve
            
        Returns:
            Dict containing task data or None if not found
        """
        task_filename = f"{task_id}.json"
        task_path = os.path.join(self.storage_dir, task_filename)
        
        if not os.path.exists(task_path):
            return None
        
        try:
            with open(task_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading task {task_id}: {e}")
            return None
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Retrieve all processed tasks
        
        Returns:
            List of all task records
        """
        tasks = []
        
        if not os.path.exists(self.storage_dir):
            return tasks
        
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                task_path = os.path.join(self.storage_dir, filename)
                try:
                    with open(task_path, 'r', encoding='utf-8') as f:
                        task_data = json.load(f)
                        tasks.append(task_data)
                except Exception as e:
                    print(f"Error reading task file {filename}: {e}")
        
        # Sort by timestamp (newest first)
        tasks.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return tasks
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a specific task
        
        Args:
            task_id: Task ID to delete
            
        Returns:
            bool: True if deleted successfully
        """
        task_filename = f"{task_id}.json"
        task_path = os.path.join(self.storage_dir, task_filename)
        
        if os.path.exists(task_path):
            try:
                os.remove(task_path)
                return True
            except Exception as e:
                print(f"Error deleting task {task_id}: {e}")
                return False
        
        return False


class CategoriesStorage:
    """Storage class for categories and their tasks"""
    def __init__(self, categories_file: str = "data/categories.json"):
        self.categories_file = categories_file
        self._ensure_categories_file()

    def _ensure_categories_file(self):
        if not os.path.exists(self.categories_file):
            # If file doesn't exist, create with empty list
            with open(self.categories_file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)

    def load_categories(self) -> List[Dict[str, Any]]:
        with open(self.categories_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_categories(self, categories: List[Dict[str, Any]]):
        with open(self.categories_file, 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=2, ensure_ascii=False)

    def add_task_to_category(self, category_id: str, task: Dict[str, Any]):
        categories = self.load_categories()
        for cat in categories:
            if str(cat.get('id')) == str(category_id):
                if 'tasks' not in cat:
                    cat['tasks'] = []
                cat['tasks'].append(task)
                break
        self.save_categories(categories)

# Global task storage instance
task_storage = TaskStorage() 

# Global categories storage instance
categories_storage = CategoriesStorage() 