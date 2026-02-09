"""
Task Model

SQLAlchemy ORM model for user tasks with Eisenhower priority matrix.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Task(Base):
    """Task model for user todo items with Eisenhower priority."""

    __tablename__ = "task"

    # Primary key - UUID string
    id: Mapped[str] = mapped_column(Text, primary_key=True)

    # Owner
    user_id: Mapped[str] = mapped_column(
        Text, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Task fields
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    due_datetime: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    priority: Mapped[str] = mapped_column(Text, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="tasks")

    # Indexes
    __table_args__ = (
        Index("task_user_id_idx", "user_id"),
        Index("task_user_completed_idx", "user_id", "is_completed"),
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, priority={self.priority})>"
