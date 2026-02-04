"""
Users Router

Endpoints for user management, session management, and RBAC.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.common import MessageResponse, PaginatedResponse, Pagination
from app.schemas.session import AccountRead, AccountsListResponse, SessionRead, SessionsListResponse
from app.schemas.user import BanUserRequest, RoleUpdate, UserRead, UserUpdate
from app.services import account as account_service
from app.services import session as session_service
from app.services import user as user_service
from app.utils.dependencies import get_active_user, require_admin, require_self_or_admin
from app.utils.exceptions import AuthorizationError, NotFoundError

router = APIRouter(prefix="/users", tags=["users"])


# ============================================================================
# User Management Endpoints
# ============================================================================


@router.get("", response_model=PaginatedResponse[UserRead])
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    role: Optional[str] = Query(None, description="Filter by role"),
    banned: Optional[bool] = Query(None, description="Filter by banned status"),
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[UserRead]:
    """
    List all users (admin only).

    Supports pagination and filtering by role and banned status.

    Returns:
        Paginated list of users.

    Raises:
        403: If not an admin.
    """
    users, total = await user_service.list_users(
        db, page=page, per_page=per_page, role=role, banned=banned
    )

    return PaginatedResponse(
        items=[UserRead.model_validate(u) for u in users],
        pagination=Pagination.create(page, per_page, total),
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: str = Path(..., description="User ID"),
    current_user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Get a user by ID (admin or self).

    Returns:
        User profile data.

    Raises:
        403: If not admin and not accessing own profile.
        404: If user not found.
    """
    # Check authorization
    if current_user.id != user_id and not current_user.is_admin:
        raise AuthorizationError(detail="Can only access your own profile or require admin role")

    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError(resource="User")

    return UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_update: UserUpdate,
    user_id: str = Path(..., description="User ID"),
    current_user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Update a user's profile (admin or self).

    Non-admin users can only update their own profile.

    Returns:
        Updated user profile.

    Raises:
        403: If not admin and not updating own profile.
        404: If user not found.
    """
    # Check authorization
    if current_user.id != user_id and not current_user.is_admin:
        raise AuthorizationError(detail="Can only update your own profile or require admin role")

    user = await user_service.update_user(db, user_id, user_update)
    if not user:
        raise NotFoundError(resource="User")

    return UserRead.model_validate(user)


# ============================================================================
# Role Management Endpoints (Admin Only)
# ============================================================================


@router.put("/{user_id}/role", response_model=UserRead)
async def update_user_role(
    role_update: RoleUpdate,
    user_id: str = Path(..., description="User ID"),
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Update a user's role (admin only).

    Returns:
        Updated user with new role.

    Raises:
        403: If not an admin.
        404: If user not found.
    """
    user = await user_service.update_user_role(db, user_id, role_update.role.value)
    if not user:
        raise NotFoundError(resource="User")

    return UserRead.model_validate(user)


@router.post("/{user_id}/ban", response_model=UserRead)
async def ban_user(
    ban_request: BanUserRequest,
    user_id: str = Path(..., description="User ID"),
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Ban a user (admin only).

    Returns:
        Updated user with banned status.

    Raises:
        403: If not an admin.
        404: If user not found.
    """
    # Prevent self-ban
    if admin.id == user_id:
        raise AuthorizationError(detail="Cannot ban yourself")

    user = await user_service.ban_user(
        db, user_id, reason=ban_request.reason, expires_at=ban_request.expires_at
    )
    if not user:
        raise NotFoundError(resource="User")

    return UserRead.model_validate(user)


@router.delete("/{user_id}/ban", response_model=UserRead)
async def unban_user(
    user_id: str = Path(..., description="User ID"),
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Unban a user (admin only).

    Returns:
        Updated user with unbanned status.

    Raises:
        403: If not an admin.
        404: If user not found.
    """
    user = await user_service.unban_user(db, user_id)
    if not user:
        raise NotFoundError(resource="User")

    return UserRead.model_validate(user)


# ============================================================================
# Session Management Endpoints
# ============================================================================


@router.get("/{user_id}/sessions", response_model=SessionsListResponse)
async def get_user_sessions(
    user_id: str = Path(..., description="User ID"),
    current_user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> SessionsListResponse:
    """
    Get all active sessions for a user (admin or self).

    Returns:
        List of active sessions.

    Raises:
        403: If not admin and not accessing own sessions.
    """
    # Check authorization
    if current_user.id != user_id and not current_user.is_admin:
        raise AuthorizationError(detail="Can only access your own sessions or require admin role")

    sessions = await session_service.get_user_sessions(db, user_id)

    return SessionsListResponse(
        sessions=[SessionRead.model_validate(s) for s in sessions],
        total=len(sessions),
    )


@router.delete("/{user_id}/sessions", response_model=MessageResponse)
async def revoke_all_sessions(
    user_id: str = Path(..., description="User ID"),
    current_user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Revoke all sessions for a user (admin or self).

    Returns:
        Success message with count of revoked sessions.

    Raises:
        403: If not admin and not revoking own sessions.
    """
    # Check authorization
    if current_user.id != user_id and not current_user.is_admin:
        raise AuthorizationError(detail="Can only revoke your own sessions or require admin role")

    count = await session_service.revoke_all_sessions(db, user_id)

    return MessageResponse(message=f"Revoked {count} session(s)")


@router.delete("/{user_id}/sessions/{session_id}", response_model=MessageResponse)
async def revoke_session(
    user_id: str = Path(..., description="User ID"),
    session_id: str = Path(..., description="Session ID"),
    current_user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Revoke a specific session (admin or self).

    Returns:
        Success message if session was revoked.

    Raises:
        403: If not admin and not revoking own session.
        404: If session not found.
    """
    # Check authorization
    if current_user.id != user_id and not current_user.is_admin:
        raise AuthorizationError(detail="Can only revoke your own sessions or require admin role")

    success = await session_service.revoke_session(db, session_id, user_id)
    if not success:
        raise NotFoundError(resource="Session")

    return MessageResponse(message="Session revoked successfully")


# ============================================================================
# Account (OAuth Provider) Endpoints
# ============================================================================


@router.get("/{user_id}/accounts", response_model=AccountsListResponse)
async def get_user_accounts(
    user_id: str = Path(..., description="User ID"),
    current_user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> AccountsListResponse:
    """
    Get linked OAuth accounts for a user (admin or self).

    Returns:
        List of linked OAuth accounts.

    Raises:
        403: If not admin and not accessing own accounts.
    """
    # Check authorization
    if current_user.id != user_id and not current_user.is_admin:
        raise AuthorizationError(detail="Can only access your own accounts or require admin role")

    accounts = await account_service.get_oauth_accounts(db, user_id)

    return AccountsListResponse(
        accounts=[AccountRead.model_validate(a) for a in accounts]
    )
