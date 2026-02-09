"""
Task Schemas

Pydantic v2 schemas for task CRUD operations per API contract.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class TaskPriority(str, Enum):
    """Eisenhower priority matrix values."""

    URGENT_IMPORTANT = "urgent_important"
    NOT_URGENT_IMPORTANT = "not_urgent_important"
    URGENT_NOT_IMPORTANT = "urgent_not_important"
    NOT_URGENT_NOT_IMPORTANT = "not_urgent_not_important"


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    due_datetime: Optional[datetime] = None
    priority: TaskPriority

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty")
        return v


class TaskRead(BaseModel):
    """Schema for reading task data."""

    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    due_datetime: Optional[datetime] = None
    priority: Optional[TaskPriority] = None
    is_completed: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Title cannot be empty")
        return v


class TaskListData(BaseModel):
    """Data envelope for task list response."""

    tasks: List[TaskRead]
    total_count: int
    limit: int
    offset: int


class TaskListResponse(BaseModel):
    """Task list response with envelope."""

    success: bool = True
    data: TaskListData
