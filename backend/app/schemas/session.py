"""
Session Schemas

Pydantic schemas for session-related API operations.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class SessionRead(BaseModel):
    """Schema for reading session data."""

    id: str
    user_id: str
    expires_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_impersonated: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class SessionsListResponse(BaseModel):
    """Response with list of sessions."""

    sessions: List[SessionRead]
    total: int


class AccountRead(BaseModel):
    """Schema for reading account (OAuth provider) data."""

    id: str
    provider_id: str
    account_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class AccountsListResponse(BaseModel):
    """Response with list of linked accounts."""

    accounts: List[AccountRead]
