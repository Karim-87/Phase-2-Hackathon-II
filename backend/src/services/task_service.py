from sqlmodel import Session, select, and_, func
from typing import List, Optional
import uuid
from datetime import datetime
from src.models.task import Task, TaskCreate, TaskUpdate, PriorityEnum
from src.schemas.task import TaskCreateRequest, TaskUpdateRequest

class TaskService:
    """
    Service class for handling task-related business logic and database operations.

    According to the Spec Constitution, this service enforces user isolation by ensuring
    that all operations are filtered by the user_id from the JWT token.
    """

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: uuid.UUID) -> Task:
        """
        Create a new task for the specified user.

        Args:
            session: Database session
            task_data: Task data to create
            user_id: ID of the user creating the task

        Returns:
            Created Task object
        """
        # Create task with user_id from JWT, not from request
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            due_datetime=task_data.due_datetime,
            priority=task_data.priority,
            is_completed=task_data.is_completed,
            user_id=user_id
        )
        db_task.created_at = datetime.utcnow()
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def get_task_by_id(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """
        Retrieve a specific task by its ID for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user requesting the task

        Returns:
            Task object if found and belongs to user, None otherwise
        """
        statement = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        task = session.exec(statement).first()
        return task

    @staticmethod
    def get_tasks_for_user(
        session: Session,
        user_id: uuid.UUID,
        priority: Optional[str] = None,
        completed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> tuple[List[Task], int]:
        """
        Retrieve all tasks for the specified user with optional filtering and pagination.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            priority: Optional priority level to filter by
            completed: Optional completion status to filter by
            limit: Maximum number of tasks to return
            offset: Number of tasks to skip
            sort_by: Field to sort by (created_at, updated_at, due_datetime, priority)
            sort_order: Sort order (asc or desc)

        Returns:
            Tuple of (list of tasks, total count)
        """
        # Build query with user isolation
        statement = select(Task).where(Task.user_id == user_id)

        # Apply filters
        if priority is not None:
            statement = statement.where(Task.priority == priority)
        if completed is not None:
            statement = statement.where(Task.is_completed == completed)

        # Apply sorting
        if sort_by == "created_at":
            statement = statement.order_by(Task.created_at.desc() if sort_order == "desc" else Task.created_at.asc())
        elif sort_by == "updated_at":
            statement = statement.order_by(Task.updated_at.desc() if sort_order == "desc" else Task.updated_at.asc())
        elif sort_by == "due_datetime":
            statement = statement.order_by(Task.due_datetime.desc() if sort_order == "desc" else Task.due_datetime.asc())
        elif sort_by == "priority":
            statement = statement.order_by(Task.priority.desc() if sort_order == "desc" else Task.priority.asc())

        # Get total count for pagination
        count_statement = select(func.count()).select_from(statement.subquery())
        total_count = session.exec(count_statement).one()

        # Apply pagination
        statement = statement.offset(offset).limit(limit)
        tasks = session.exec(statement).all()

        return tasks, total_count

    @staticmethod
    def update_task(session: Session, task_id: uuid.UUID, task_update: TaskUpdate, user_id: uuid.UUID) -> Optional[Task]:
        """
        Update an existing task for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to update
            task_update: Update data
            user_id: ID of the user requesting the update

        Returns:
            Updated Task object if successful and belongs to user, None otherwise
        """
        statement = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        db_task = session.exec(statement).first()

        if not db_task:
            return None

        # Update fields that are provided
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)

        # Update the timestamp
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def update_task_completion(session: Session, task_id: uuid.UUID, completed: bool, user_id: uuid.UUID) -> Optional[Task]:
        """
        Update only the completion status of a task for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to update
            completed: New completion status
            user_id: ID of the user requesting the update

        Returns:
            Updated Task object if successful and belongs to user, None otherwise
        """
        statement = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        db_task = session.exec(statement).first()

        if not db_task:
            return None

        db_task.is_completed = completed
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """
        Delete a task for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user requesting the deletion

        Returns:
            True if deletion was successful, False otherwise
        """
        statement = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        db_task = session.exec(statement).first()

        if not db_task:
            return False

        session.delete(db_task)
        session.commit()
        return True