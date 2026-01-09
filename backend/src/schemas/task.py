from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from src.models.task import TaskRead, TaskCreate, TaskUpdate

class TaskResponse(BaseModel):
    """
    Standard response wrapper for task operations.
    """
    success: bool
    data: Optional[TaskRead] = None

class TaskListResponse(BaseModel):
    """
    Standard response wrapper for listing tasks.
    """
    success: bool
    data: dict

    class Config:
        from_attributes = True

class TaskCreateRequest(BaseModel):
    """
    Request schema for creating a new task.
    """
    title: str
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: str  # Will be validated against PriorityEnum in the endpoint
    is_completed: Optional[bool] = False

class TaskUpdateRequest(BaseModel):
    """
    Request schema for updating an existing task.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: Optional[str] = None  # Will be validated against PriorityEnum in the endpoint
    is_completed: Optional[bool] = None

class TaskCompletionRequest(BaseModel):
    """
    Request schema for updating task completion status.
    """
    completed: bool

class TaskCompletionResponse(BaseModel):
    """
    Response schema for task completion updates.
    """
    success: bool
    data: Optional[TaskRead] = None