"""
Custom Exception Handlers

Custom HTTP exceptions with error codes for consistent error responses.
"""

from typing import Any, Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


class AppException(HTTPException):
    """Base application exception with error code support."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code


class AuthenticationError(AppException):
    """Raised when authentication fails."""

    def __init__(
        self,
        detail: str = "Could not validate credentials",
        error_code: str = "AUTH_INVALID_CREDENTIALS",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(AppException):
    """Raised when user lacks required permissions."""

    def __init__(
        self,
        detail: str = "Insufficient permissions",
        error_code: str = "AUTH_FORBIDDEN",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code,
        )


class NotFoundError(AppException):
    """Raised when a resource is not found."""

    def __init__(
        self,
        resource: str = "Resource",
        error_code: str = "NOT_FOUND",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
            error_code=error_code,
        )


class BadRequestError(AppException):
    """Raised for invalid requests."""

    def __init__(
        self,
        detail: str = "Invalid request",
        error_code: str = "BAD_REQUEST",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code,
        )


class ValidationError(AppException):
    """Raised for validation errors."""

    def __init__(
        self,
        detail: str = "Validation failed",
        error_code: str = "VALIDATION_ERROR",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code=error_code,
        )


class UserBannedError(AppException):
    """Raised when a banned user attempts to access the system."""

    def __init__(
        self,
        detail: str = "User account is banned",
        error_code: str = "USER_BANNED",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code,
        )


class EmailNotVerifiedError(AppException):
    """Raised when email verification is required."""

    def __init__(
        self,
        detail: str = "Email verification required",
        error_code: str = "EMAIL_NOT_VERIFIED",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code,
        )


# Error codes for reference
ERROR_CODES = {
    # Authentication errors
    "AUTH_INVALID_CREDENTIALS": "Invalid or expired credentials",
    "AUTH_TOKEN_EXPIRED": "Authentication token has expired",
    "AUTH_TOKEN_INVALID": "Invalid authentication token",
    "AUTH_MISSING_TOKEN": "Authentication token not provided",
    "AUTH_FORBIDDEN": "Insufficient permissions for this action",
    # User errors
    "USER_NOT_FOUND": "User not found",
    "USER_BANNED": "User account is banned",
    "EMAIL_NOT_VERIFIED": "Email verification is required",
    "USER_ALREADY_EXISTS": "User with this email already exists",
    # Session errors
    "SESSION_NOT_FOUND": "Session not found",
    "SESSION_EXPIRED": "Session has expired",
    # General errors
    "NOT_FOUND": "Resource not found",
    "BAD_REQUEST": "Invalid request",
    "VALIDATION_ERROR": "Request validation failed",
    "INTERNAL_ERROR": "Internal server error",
}


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Custom exception handler for AppException."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "error_code": exc.error_code,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Custom exception handler for HTTPException."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "error_code": None,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Generic exception handler for unhandled exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "error_code": "INTERNAL_ERROR",
        },
    )
