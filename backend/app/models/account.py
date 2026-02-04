"""
Account Model

Better-Auth compatible Account model for OAuth provider linkages
and credential storage.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Index, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Account(Base):
    """
    Account model for OAuth providers and credentials.

    Stores OAuth tokens and password hashes for the 'credential' provider.
    """

    __tablename__ = "account"

    # Primary key
    id: Mapped[str] = mapped_column(Text, primary_key=True)

    # Foreign key to user
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Provider identification
    account_id: Mapped[str] = mapped_column(Text, nullable=False)
    provider_id: Mapped[str] = mapped_column(Text, nullable=False)

    # OAuth tokens
    access_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    id_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Token expiration
    access_token_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    refresh_token_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # OAuth scope
    scope: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Password (for credential provider only)
    password: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

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
    user: Mapped["User"] = relationship("User", back_populates="accounts")

    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint("provider_id", "account_id", name="uq_account_provider"),
        Index("account_user_id_idx", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<Account(id={self.id}, provider={self.provider_id}, user_id={self.user_id})>"

    @property
    def is_oauth(self) -> bool:
        """Check if this is an OAuth account."""
        return self.provider_id != "credential"

    @property
    def is_credential(self) -> bool:
        """Check if this is a credential (password) account."""
        return self.provider_id == "credential"
