"""
FastAPI Dependencies

Authentication and authorization dependencies for route protection.
"""

from typing import Optional

from fastapi import Depends, Header
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.services.auth import verify_jwt
from app.utils.exceptions import (
    AuthenticationError,
    AuthorizationError,
    EmailNotVerifiedError,
    NotFoundError,
    UserBannedError,
)


async def get_token_from_header(
    authorization: Optional[str] = Header(None, alias="Authorization"),
) -> str:
    """
    Extract JWT token from Authorization header.

    Args:
        authorization: Authorization header value.

    Returns:
        JWT token string.

    Raises:
        AuthenticationError: If token is missing or malformed.
    """
    if not authorization:
        raise AuthenticationError(
            detail="Authorization header missing",
            error_code="AUTH_MISSING_TOKEN",
        )

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AuthenticationError(
            detail="Invalid authorization header format. Use: Bearer <token>",
            error_code="AUTH_INVALID_FORMAT",
        )

    return parts[1]


async def get_current_user_id(
    token: str = Depends(get_token_from_header),
) -> str:
    """
    Verify JWT and extract user ID.

    Args:
        token: JWT token from header.

    Returns:
        User ID from token payload.

    Raises:
        AuthenticationError: If token is invalid or expired.
    """
    try:
        payload = await verify_jwt(token)
        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError(
                detail="Token missing user ID",
                error_code="AUTH_INVALID_TOKEN",
            )
        return user_id
    except JWTError as e:
        raise AuthenticationError(
            detail=str(e),
            error_code="AUTH_TOKEN_INVALID",
        )


async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Get the current authenticated user from database.

    Args:
        user_id: User ID from JWT.
        db: Database session.

    Returns:
        User model instance.

    Raises:
        NotFoundError: If user not found in database.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise NotFoundError(resource="User", error_code="USER_NOT_FOUND")

    return user


async def require_verified_email(
    user: User = Depends(get_current_user),
) -> User:
    """
    Require that the user has verified their email.

    Args:
        user: Current authenticated user.

    Returns:
        User if email is verified.

    Raises:
        EmailNotVerifiedError: If email is not verified.
    """
    if not user.email_verified:
        raise EmailNotVerifiedError()
    return user


async def check_user_not_banned(
    user: User = Depends(get_current_user),
) -> User:
    """
    Check that the user is not banned.

    Args:
        user: Current authenticated user.

    Returns:
        User if not banned.

    Raises:
        UserBannedError: If user is banned.
    """
    if user.is_banned_active:
        detail = "User account is banned"
        if user.ban_reason:
            detail = f"{detail}: {user.ban_reason}"
        raise UserBannedError(detail=detail)
    return user


async def get_active_user(
    user: User = Depends(check_user_not_banned),
) -> User:
    """
    Get current user ensuring they are not banned.

    Combines authentication and ban check.

    Args:
        user: User after ban check.

    Returns:
        Active, non-banned user.
    """
    return user


async def require_admin(
    user: User = Depends(get_active_user),
) -> User:
    """
    Require that the current user has admin role.

    Args:
        user: Current active user.

    Returns:
        User if they are an admin.

    Raises:
        AuthorizationError: If user is not an admin.
    """
    if not user.is_admin:
        raise AuthorizationError(
            detail="Admin access required",
            error_code="AUTH_FORBIDDEN",
        )
    return user


def require_role(allowed_roles: list[str]):
    """
    Create a dependency that requires specific roles.

    Args:
        allowed_roles: List of allowed role names.

    Returns:
        Dependency function that checks role.
    """

    async def role_checker(user: User = Depends(get_active_user)) -> User:
        if user.role not in allowed_roles:
            raise AuthorizationError(
                detail=f"Required role: {', '.join(allowed_roles)}",
                error_code="AUTH_FORBIDDEN",
            )
        return user

    return role_checker


async def require_self_or_admin(
    target_user_id: str,
    user: User = Depends(get_active_user),
) -> User:
    """
    Require that user is either accessing their own data or is an admin.

    Args:
        target_user_id: ID of the user being accessed.
        user: Current authenticated user.

    Returns:
        User if they have access.

    Raises:
        AuthorizationError: If user doesn't have access.
    """
    if user.id != target_user_id and not user.is_admin:
        raise AuthorizationError(
            detail="Can only access your own data or require admin role",
            error_code="AUTH_FORBIDDEN",
        )
    return user
