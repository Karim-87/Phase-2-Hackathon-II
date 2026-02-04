"""
Pydantic Schemas Package

Request and response schemas for API validation.
"""

from app.schemas.common import (
    ErrorResponse,
    MessageResponse,
    PaginatedResponse,
    Pagination,
    SuccessResponse,
)
from app.schemas.user import (
    BanUserRequest,
    RoleUpdate,
    UserCreate,
    UserRead,
    UserUpdate,
)

__all__ = [
    # Common
    "ErrorResponse",
    "MessageResponse",
    "PaginatedResponse",
    "Pagination",
    "SuccessResponse",
    # User
    "BanUserRequest",
    "RoleUpdate",
    "UserCreate",
    "UserRead",
    "UserUpdate",
]
