"""
Session Model

Better-Auth compatible Session model for tracking active user sessions.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Index, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Session(Base):
    """
    Session model representing active user sessions.

    Managed by Better-Auth, read by FastAPI for session validation.
    """

    __tablename__ = "session"

    # Primary key
    id: Mapped[str] = mapped_column(Text, primary_key=True)

    # Foreign key to user
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Session token
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    # Expiration
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Client information
    ip_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Admin impersonation tracking
    impersonated_by: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

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
    user: Mapped["User"] = relationship("User", back_populates="sessions")

    # Indexes
    __table_args__ = (
        Index("session_user_id_idx", "user_id"),
        Index("session_token_idx", "token"),
    )

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>"

    @property
    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.now(self.expires_at.tzinfo) > self.expires_at

    @property
    def is_impersonated(self) -> bool:
        """Check if session is an impersonation session."""
        return self.impersonated_by is not None
