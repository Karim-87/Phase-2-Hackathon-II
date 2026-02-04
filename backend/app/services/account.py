"""
Account Service

Functions for managing OAuth account linkages.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account


async def get_user_accounts(
    db: AsyncSession,
    user_id: str,
) -> List[Account]:
    """
    Get all linked accounts for a user.

    Args:
        db: Database session.
        user_id: ID of the user.

    Returns:
        List of Account objects linked to the user.
    """
    result = await db.execute(
        select(Account)
        .where(Account.user_id == user_id)
        .order_by(Account.created_at.desc())
    )
    return list(result.scalars().all())


async def get_account_by_provider(
    db: AsyncSession,
    user_id: str,
    provider_id: str,
) -> Optional[Account]:
    """
    Get a specific provider account for a user.

    Args:
        db: Database session.
        user_id: ID of the user.
        provider_id: Provider identifier (e.g., 'google', 'github').

    Returns:
        Account if found, None otherwise.
    """
    result = await db.execute(
        select(Account)
        .where(Account.user_id == user_id)
        .where(Account.provider_id == provider_id)
    )
    return result.scalar_one_or_none()


async def get_account_by_id(
    db: AsyncSession,
    account_id: str,
) -> Optional[Account]:
    """
    Get an account by its ID.

    Args:
        db: Database session.
        account_id: ID of the account.

    Returns:
        Account if found, None otherwise.
    """
    result = await db.execute(
        select(Account).where(Account.id == account_id)
    )
    return result.scalar_one_or_none()


async def get_oauth_accounts(
    db: AsyncSession,
    user_id: str,
) -> List[Account]:
    """
    Get only OAuth accounts for a user (excludes credential accounts).

    Args:
        db: Database session.
        user_id: ID of the user.

    Returns:
        List of OAuth Account objects.
    """
    result = await db.execute(
        select(Account)
        .where(Account.user_id == user_id)
        .where(Account.provider_id != "credential")
        .order_by(Account.created_at.desc())
    )
    return list(result.scalars().all())
