from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
import uuid
from datetime import datetime

from src.database.session import get_session
from src.auth.dependencies import get_current_user
from src.services.task_service import TaskService
from src.models.task import Task, TaskCreate, TaskUpdate, PriorityEnum
from src.schemas.task import (
    TaskResponse,
    TaskListResponse,
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskCompletionRequest,
    TaskCompletionResponse
)

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_request: TaskCreateRequest,
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    According to the Spec Constitution, the user_id is derived from the JWT token
    and never accepted from the request body or URL parameters.
    """
    # Validate priority value
    try:
        priority = PriorityEnum(task_request.priority)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid priority value. Must be one of: {[e.value for e in PriorityEnum]}"
        )

    # Prepare task data
    task_data = TaskCreate(
        title=task_request.title,
        description=task_request.description,
        due_datetime=task_request.due_datetime,
        priority=priority,
        is_completed=task_request.is_completed
    )

    # Create task with user_id from JWT token
    db_task = TaskService.create_task(session, task_data, current_user_id)

    return TaskResponse(success=True, data=db_task)


@router.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session),
    priority: Optional[str] = Query(None, description="Filter by priority level"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)")
):
    """
    Retrieve all tasks for the authenticated user with optional filtering and pagination.
    """
    # Validate sort parameters
    valid_sort_fields = ["created_at", "updated_at", "due_datetime", "priority", "title"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort_by field. Must be one of: {valid_sort_fields}"
        )

    valid_sort_orders = ["asc", "desc"]
    if sort_order not in valid_sort_orders:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort_order. Must be one of: {valid_sort_orders}"
        )

    # Validate priority if provided
    if priority is not None:
        try:
            PriorityEnum(priority)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid priority value. Must be one of: {[e.value for e in PriorityEnum]}"
            )

    # Get tasks for the current user
    tasks, total_count = TaskService.get_tasks_for_user(
        session=session,
        user_id=current_user_id,
        priority=priority,
        completed=completed,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order
    )

    return TaskListResponse(
        success=True,
        data={
            "tasks": tasks,
            "total_count": total_count,
            "limit": limit,
            "offset": offset
        }
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task for the authenticated user.

    According to the Spec Constitution, if a task exists but belongs to another user,
    return 404 to prevent user enumeration.
    """
    db_task = TaskService.get_task_by_id(session, task_id, current_user_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(success=True, data=db_task)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: uuid.UUID,
    task_request: TaskUpdateRequest,
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task for the authenticated user.
    """
    # Validate priority if provided
    if task_request.priority is not None:
        try:
            PriorityEnum(task_request.priority)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid priority value. Must be one of: {[e.value for e in PriorityEnum]}"
            )

    # Prepare update data
    task_update = TaskUpdate(
        title=task_request.title,
        description=task_request.description,
        due_datetime=task_request.due_datetime,
        priority=task_request.priority,
        is_completed=task_request.is_completed
    )

    # Attempt to update the task
    updated_task = TaskService.update_task(session, task_id, task_update, current_user_id)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return TaskResponse(success=True, data=updated_task)


@router.patch("/tasks/{task_id}/complete", response_model=TaskCompletionResponse)
def update_task_completion(
    task_id: uuid.UUID,
    completion_request: TaskCompletionRequest,
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update only the completion status of a task for the authenticated user.
    """
    # Update task completion status
    updated_task = TaskService.update_task_completion(
        session,
        task_id,
        completion_request.completed,
        current_user_id
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return TaskCompletionResponse(success=True, data=updated_task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task for the authenticated user.
    """
    success = TaskService.delete_task(session, task_id, current_user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    # Return 204 No Content on successful deletion
    return