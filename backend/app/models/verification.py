"""
Verification Model

Better-Auth compatible Verification model for email verification
and password reset tokens.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Verification(Base):
    """
    Verification model for email verification and password reset tokens.

    Managed by Better-Auth for verification flows.
    """

    __tablename__ = "verification"

    # Primary key
    id: Mapped[str] = mapped_column(Text, primary_key=True)

    # Verification target (email address)
    identifier: Mapped[str] = mapped_column(Text, nullable=False, index=True)

    # Verification token/code
    value: Mapped[str] = mapped_column(Text, nullable=False)

    # Expiration
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Timestamps
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Indexes
    __table_args__ = (
        Index("verification_identifier_idx", "identifier"),
    )

    def __repr__(self) -> str:
        return f"<Verification(id={self.id}, identifier={self.identifier})>"

    @property
    def is_expired(self) -> bool:
        """Check if verification token has expired."""
        return datetime.now(self.expires_at.tzinfo) > self.expires_at
