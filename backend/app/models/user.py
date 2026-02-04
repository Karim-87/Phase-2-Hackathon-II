"""
User Model

Better-Auth compatible User model following the standard schema.
Stores user profile, role, and ban status.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Index, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.session import Session


class User(Base):
    """
    User model representing authenticated users.

    Schema follows Better-Auth conventions for compatibility
    with shared database architecture.
    """

    __tablename__ = "user"

    # Primary key - Better-Auth uses TEXT IDs (ULID or UUID string)
    id: Mapped[str] = mapped_column(Text, primary_key=True)

    # Core fields
    email: Mapped[str] = mapped_column(
        Text, unique=True, nullable=False, index=True
    )
    email_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Role-based access control
    role: Mapped[str] = mapped_column(Text, default="user")

    # Ban management
    banned: Mapped[bool] = mapped_column(Boolean, default=False)
    ban_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ban_expires: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

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
    sessions: Mapped[List["Session"]] = relationship(
        "Session", back_populates="user", cascade="all, delete-orphan"
    )
    accounts: Mapped[List["Account"]] = relationship(
        "Account", back_populates="user", cascade="all, delete-orphan"
    )

    # Indexes
    __table_args__ = (
        Index("user_email_idx", "email"),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == "admin"

    @property
    def is_banned_active(self) -> bool:
        """Check if user is currently banned (considering expiration)."""
        if not self.banned:
            return False
        if self.ban_expires is None:
            return True
        return datetime.now(self.ban_expires.tzinfo) < self.ban_expires
