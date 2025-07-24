"""
Task model for VoiceTaskAI
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Base task model"""
    title: str = Field(..., description="Task title/description")
    assignee: str = Field(..., description="Person assigned to the task")
    project: Optional[str] = Field(None, description="Project name")
    deadline: Optional[datetime] = Field(None, description="Task deadline")
    priority: Optional[str] = Field("medium", description="Task priority (low/medium/high)")
    status: Optional[str] = Field("pending", description="Task status")


class TaskCreate(TaskBase):
    """Task creation model"""
    pass


class Task(TaskBase):
    """Complete task model with ID and timestamps"""
    id: str = Field(..., description="Unique task identifier")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "task_123",
                "title": "Review Q3 report",
                "assignee": "Alex",
                "project": "Project Mercury",
                "deadline": "2024-12-20T17:00:00",
                "priority": "high",
                "status": "pending",
                "created_at": "2024-12-15T10:30:00",
                "updated_at": "2024-12-15T10:30:00"
            }
        }


class TaskResponse(BaseModel):
    """Task response model"""
    task: Task
    message: str = "Task created successfully"
