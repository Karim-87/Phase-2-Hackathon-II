from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class UserResponse(BaseModel):
    """
    Response model for user-related operations.
    """
    success: bool
    data: Optional['UserData'] = None
    message: Optional[str] = None


class UserData(BaseModel):
    """
    Data model for user information in API responses.
    """
    user_id: uuid.UUID
    email: str
    name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    token: Optional[str] = None  # JWT token for authentication


class UserListResponse(BaseModel):
    """
    Response model for listing users.
    """
    success: bool
    data: Optional[dict] = None  # Contains 'users' list and 'total_count'
    message: Optional[str] = None


class UserCreateRequest(BaseModel):
    """
    Request model for creating a new user.
    """
    email: str
    password: str
    name: Optional[str] = None


class UserUpdateRequest(BaseModel):
    """
    Request model for updating an existing user.
    """
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserLoginRequest(BaseModel):
    """
    Request model for user login.
    """
    email: str
    password: str


class UserLoginResponse(BaseModel):
    """
    Response model for user login.
    """
    success: bool
    data: Optional[UserData] = None
    message: Optional[str] = None


class UserLogoutRequest(BaseModel):
    """
    Request model for user logout.
    """
    token: str


class UserLogoutResponse(BaseModel):
    """
    Response model for user logout.
    """
    success: bool
    message: Optional[str] = None