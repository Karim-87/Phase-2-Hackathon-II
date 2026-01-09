from sqlmodel import SQLModel, Field, Column, create_engine, Session
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy import Column as sa_Column
from sqlalchemy import Enum as sa_Enum
from typing import Optional
from datetime import datetime
import uuid
import enum

class PriorityEnum(str, enum.Enum):
    """
    Priority levels based on the Eisenhower Matrix:
    - urgent_important: Do First - Important and urgent tasks
    - not_urgent_important: Schedule - Important but not urgent tasks
    - urgent_not_important: Delegate - Urgent but not important tasks
    - not_urgent_not_important: Eliminate - Neither urgent nor important tasks
    """
    URGENT_IMPORTANT = "urgent_important"
    NOT_URGENT_IMPORTANT = "not_urgent_important"
    URGENT_NOT_IMPORTANT = "urgent_not_important"
    NOT_URGENT_NOT_IMPORTANT = "not_urgent_not_important"

class TaskBase(SQLModel):
    """
    Base class for Task model containing common fields.
    This class is used for both creating and reading tasks.
    """
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    due_datetime: Optional[datetime] = Field(default=None)
    priority: PriorityEnum = Field(sa_column=sa_Column(sa_Enum(PriorityEnum), nullable=False))
    is_completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model representing a user's task in the database.

    According to the Spec Constitution, the user_id is derived exclusively from the JWT token
    and is never accepted from URL parameters or request body.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(nullable=False, index=True)  # Index for efficient filtering by user
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class TaskRead(TaskBase):
    """
    Schema for reading a task, including the ID and timestamps.
    """
    id: uuid.UUID
    user_id: uuid.UUID  # Included for transparency but not modifiable
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    The user_id is derived from the JWT token, not from the request body.
    """
    pass


class TaskUpdate(SQLModel):
    """
    Schema for updating an existing task.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    is_completed: Optional[bool] = None