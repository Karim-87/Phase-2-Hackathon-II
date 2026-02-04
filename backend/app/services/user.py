"""
User Service

Functions for user management, including CRUD, role management, and banning.
"""

from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserUpdate


async def get_user_by_id(
    db: AsyncSession,
    user_id: str,
) -> Optional[User]:
    """
    Get a user by their ID.

    Args:
        db: Database session.
        user_id: ID of the user.

    Returns:
        User if found, None otherwise.
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> Optional[User]:
    """
    Get a user by their email address.

    Args:
        db: Database session.
        email: Email address.

    Returns:
        User if found, None otherwise.
    """
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def list_users(
    db: AsyncSession,
    page: int = 1,
    per_page: int = 20,
    role: Optional[str] = None,
    banned: Optional[bool] = None,
) -> Tuple[List[User], int]:
    """
    List users with pagination and optional filters.

    Args:
        db: Database session.
        page: Page number (1-indexed).
        per_page: Items per page.
        role: Filter by role.
        banned: Filter by banned status.

    Returns:
        Tuple of (list of users, total count).
    """
    # Build base query
    query = select(User)
    count_query = select(func.count()).select_from(User)

    # Apply filters
    if role:
        query = query.where(User.role == role)
        count_query = count_query.where(User.role == role)

    if banned is not None:
        query = query.where(User.banned == banned)
        count_query = count_query.where(User.banned == banned)

    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Apply pagination
    offset = (page - 1) * per_page
    query = query.order_by(User.created_at.desc()).offset(offset).limit(per_page)

    # Execute query
    result = await db.execute(query)
    users = list(result.scalars().all())

    return users, total


async def update_user(
    db: AsyncSession,
    user_id: str,
    user_update: UserUpdate,
) -> Optional[User]:
    """
    Update a user's profile.

    Args:
        db: Database session.
        user_id: ID of the user to update.
        user_update: Update data.

    Returns:
        Updated User if found, None otherwise.
    """
    # Get existing user
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    # Update fields
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    user.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_role(
    db: AsyncSession,
    user_id: str,
    new_role: str,
) -> Optional[User]:
    """
    Update a user's role.

    Args:
        db: Database session.
        user_id: ID of the user.
        new_role: New role to assign.

    Returns:
        Updated User if found, None otherwise.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    user.role = new_role
    user.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)
    return user


async def ban_user(
    db: AsyncSession,
    user_id: str,
    reason: Optional[str] = None,
    expires_at: Optional[datetime] = None,
) -> Optional[User]:
    """
    Ban a user.

    Args:
        db: Database session.
        user_id: ID of the user to ban.
        reason: Optional ban reason.
        expires_at: Optional ban expiration timestamp.

    Returns:
        Updated User if found, None otherwise.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    user.banned = True
    user.ban_reason = reason
    user.ban_expires = expires_at
    user.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)
    return user


async def unban_user(
    db: AsyncSession,
    user_id: str,
) -> Optional[User]:
    """
    Unban a user.

    Args:
        db: Database session.
        user_id: ID of the user to unban.

    Returns:
        Updated User if found, None otherwise.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    user.banned = False
    user.ban_reason = None
    user.ban_expires = None
    user.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)
    return user


async def count_users(
    db: AsyncSession,
    role: Optional[str] = None,
) -> int:
    """
    Count total users, optionally filtered by role.

    Args:
        db: Database session.
        role: Optional role filter.

    Returns:
        Count of users.
    """
    query = select(func.count()).select_from(User)
    if role:
        query = query.where(User.role == role)
    result = await db.execute(query)
    return result.scalar() or 0
