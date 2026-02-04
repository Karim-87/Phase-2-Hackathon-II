"""
Common Schemas

Shared Pydantic schemas for API responses, errors, and pagination.
"""

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel):
    """Standard success response."""

    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[Any] = None


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    error: str
    error_code: Optional[str] = None
    details: Optional[dict[str, Any]] = None


class Pagination(BaseModel):
    """Pagination metadata."""

    page: int = Field(ge=1, default=1, description="Current page number")
    per_page: int = Field(ge=1, le=100, default=20, description="Items per page")
    total: int = Field(ge=0, description="Total number of items")
    total_pages: int = Field(ge=0, description="Total number of pages")

    @classmethod
    def create(cls, page: int, per_page: int, total: int) -> "Pagination":
        """Create pagination metadata from counts."""
        total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0
        return cls(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages,
        )


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response with items and metadata."""

    items: List[T]
    pagination: Pagination

    class Config:
        arbitrary_types_allowed = True
