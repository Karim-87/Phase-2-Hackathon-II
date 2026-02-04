from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String
from typing import Optional
import uuid
from datetime import datetime


class UserBase(SQLModel):
    """
    Base class for User model containing common fields.
    This class is used for both creating and reading users.
    """
    email: str = Field(sa_column=Column(String, unique=True, nullable=False, index=True))
    name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """
    User model representing a user in the database.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class UserRead(UserBase):
    """
    Schema for reading a user, including the ID and timestamps.
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    Includes password which should be hashed before storing.
    """
    password: str
    name: Optional[str] = None


class UserUpdate(SQLModel):
    """
    Schema for updating an existing user.
    All fields are optional to allow partial updates.
    """
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None