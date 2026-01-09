# Data Model: Todo Backend API

**Date**: 2026-01-09
**Feature**: 001-todo-backend-api
**Related**: specs/001-todo-backend-api/spec.md, specs/001-todo-backend-api/plan.md

## Overview

This document defines the data model for the Todo Backend API, focusing on the Task entity and its relationship to user authentication via JWT tokens.

## Entity Definitions

### Task Entity

The Task entity represents a user's task with the following attributes:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID/GUID | Primary Key, Auto-generated | Unique identifier for the task |
| user_id | UUID/GUID | Foreign Key, Not Null | User identifier derived from JWT token |
| title | String | Not Null, Max 255 chars | Task title/description |
| description | Text | Nullable | Detailed task description |
| due_datetime | DateTime | Nullable | Due date and time for the task |
| priority | String/Enum | Not Null | Priority level based on Eisenhower Matrix (urgent_important, not_urgent_important, urgent_not_important, not_urgent_not_important) |
| is_completed | Boolean | Not Null, Default False | Completion status of the task |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when task was created |
| updated_at | DateTime | Not Null, Auto-generated | Timestamp when task was last updated |

#### Priority Enum Values (Eisenhower Matrix)
- `urgent_important` - Do First: Important and urgent tasks
- `not_urgent_important` - Schedule: Important but not urgent tasks
- `urgent_not_important` - Delegate: Urgent but not important tasks
- `not_urgent_not_important` - Eliminate: Neither urgent nor important tasks

## Database Schema

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_datetime TIMESTAMP WITH TIME ZONE,
    priority VARCHAR(30) NOT NULL CHECK (priority IN ('urgent_important', 'not_urgent_important', 'urgent_not_important', 'not_urgent_not_important')),
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for user_id to optimize user-based queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for priority to optimize filtering
CREATE INDEX idx_tasks_priority ON tasks(priority);

-- Index for completion status to optimize filtering
CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);

-- Index for due date to optimize date-based queries
CREATE INDEX idx_tasks_due_datetime ON tasks(due_datetime);
```

## Relationships

### Task to User Relationship
- One-to-many relationship between User and Task entities
- The user_id field in the Task table references the user identified in the JWT token
- User identity is derived exclusively from the JWT token, not from URL parameters or request body

## SQLModel Implementation

```python
from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    due_datetime: Optional[datetime] = Field(default=None)
    priority: str = Field(
        sa_column=Column(
            "priority",
            sa.Enum("urgent_important", "not_urgent_important", "urgent_not_important", "not_urgent_not_important", name="priority_enum"),
            nullable=False
        )
    )
    is_completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: Optional[str] = None
    is_completed: Optional[bool] = None
```

## Security Considerations

### Data Access Control
- The user_id is never accepted from request body or URL parameters
- The user_id is exclusively derived from the JWT token
- All database queries are filtered by the user_id from the JWT token
- Users can only access tasks where user_id matches their JWT identity

### Privacy Protection
- When a user attempts to access a task that exists but belongs to another user, the API returns 404 Not Found to prevent user enumeration
- No direct user-to-user access is allowed through the API

## Indexing Strategy

1. **Primary Index**: id (UUID) - For direct task access
2. **User Access Index**: user_id - For filtering tasks by authenticated user
3. **Query Optimization Indexes**:
   - priority: For filtering by Eisenhower Matrix priority
   - is_completed: For filtering by completion status
   - due_datetime: For date-based queries and sorting

## Constraints

1. **Referential Integrity**: The user_id must correspond to a valid user identity from JWT
2. **Data Validation**: Priority field restricted to valid Eisenhower Matrix values
3. **NotNull Constraints**: Critical fields (id, user_id, title, priority, is_completed) have not-null constraints
4. **Length Constraints**: Title limited to 255 characters to prevent abuse

## Migration Strategy

Initial schema creation will use Alembic migrations with the following steps:
1. Create the tasks table with all required columns
2. Add indexes for performance optimization
3. Set up proper constraints and checks
4. Configure default values for timestamps and completion status