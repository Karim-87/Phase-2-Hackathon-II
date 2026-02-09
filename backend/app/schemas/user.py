"""
User Schemas

Pydantic schemas for user-related API operations.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    name: Optional[str] = Field(None, max_length=100)
    image: Optional[str] = Field(None, max_length=500)


class UserCreate(UserBase):
    """Schema for creating a new user (used by Better-Auth)."""

    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        import re
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least 1 uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least 1 lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least 1 number")
        return v


class UserRead(BaseModel):
    """Schema for reading user data."""

    id: str
    email: str
    email_verified: bool
    name: Optional[str] = None
    image: Optional[str] = None
    role: str = "user"
    banned: bool = False
    ban_reason: Optional[str] = None
    ban_expires: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    name: Optional[str] = Field(None, max_length=100)
    image: Optional[str] = Field(None, max_length=500)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v.strip()) == 0:
            raise ValueError("Name cannot be empty")
        return v


class RoleUpdate(BaseModel):
    """Schema for updating user role (admin only)."""

    role: UserRole = Field(..., description="New role for the user")


class BanUserRequest(BaseModel):
    """Schema for banning a user (admin only)."""

    reason: Optional[str] = Field(None, max_length=500, description="Reason for the ban")
    expires_at: Optional[datetime] = Field(
        None, description="Ban expiration timestamp (null for permanent)"
    )

    @field_validator("expires_at")
    @classmethod
    def validate_expires_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v <= datetime.now(v.tzinfo):
            raise ValueError("Ban expiration must be in the future")
        return v


class UserPublic(BaseModel):
    """Public user information (limited fields)."""

    id: str
    name: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True
