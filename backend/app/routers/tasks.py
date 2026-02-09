"""
Task CRUD Router

Endpoints for creating, reading, updating, and deleting tasks.
All endpoints scoped to the authenticated user.
"""

import secrets
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.task import (
    TaskCreate,
    TaskListData,
    TaskListResponse,
    TaskPriority,
    TaskRead,
    TaskUpdate,
)
from app.utils.dependencies import get_active_user
from app.utils.exceptions import NotFoundError

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    priority: Optional[TaskPriority] = Query(None),
    is_completed: Optional[bool] = Query(None),
    sort_by: str = Query("created_at", pattern="^(created_at|updated_at|due_datetime|priority|title)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> TaskListResponse:
    """List authenticated user's tasks with optional filtering."""
    query = select(Task).where(Task.user_id == user.id)

    if priority is not None:
        query = query.where(Task.priority == priority.value)
    if is_completed is not None:
        query = query.where(Task.is_completed == is_completed)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total_count = total_result.scalar() or 0

    # Sort
    sort_column = getattr(Task, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Paginate
    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    tasks = result.scalars().all()

    return TaskListResponse(
        success=True,
        data=TaskListData(
            tasks=[TaskRead.model_validate(t) for t in tasks],
            total_count=total_count,
            limit=limit,
            offset=offset,
        ),
    )


@router.post("", response_model=SuccessResponse, status_code=201)
async def create_task(
    request: TaskCreate,
    user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse:
    """Create a new task for the authenticated user."""
    task = Task(
        id=secrets.token_hex(16),
        user_id=user.id,
        title=request.title,
        description=request.description,
        due_datetime=request.due_datetime,
        priority=request.priority.value,
        is_completed=False,
    )
    db.add(task)
    await db.flush()
    await db.refresh(task)

    return SuccessResponse(
        success=True,
        message="Task created successfully",
        data=TaskRead.model_validate(task).model_dump(mode="json"),
    )


@router.get("/{task_id}", response_model=SuccessResponse)
async def get_task(
    task_id: str,
    user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse:
    """Get a task by ID (must belong to authenticated user)."""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user.id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise NotFoundError("Task not found")

    return SuccessResponse(
        success=True,
        data=TaskRead.model_validate(task).model_dump(mode="json"),
    )


@router.patch("/{task_id}", response_model=SuccessResponse)
async def update_task(
    task_id: str,
    request: TaskUpdate,
    user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse:
    """Update a task (must belong to authenticated user)."""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user.id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise NotFoundError("Task not found")

    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "priority" and value is not None:
            value = value.value if hasattr(value, "value") else value
        setattr(task, field, value)

    await db.flush()
    await db.refresh(task)

    return SuccessResponse(
        success=True,
        message="Task updated successfully",
        data=TaskRead.model_validate(task).model_dump(mode="json"),
    )


@router.delete("/{task_id}", response_model=SuccessResponse)
async def delete_task(
    task_id: str,
    user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse:
    """Delete a task (must belong to authenticated user)."""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user.id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise NotFoundError("Task not found")

    await db.delete(task)

    return SuccessResponse(
        success=True,
        message="Task deleted successfully",
    )
