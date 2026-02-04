"""
Session Service

Functions for managing user sessions.
"""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import Session


async def get_user_sessions(
    db: AsyncSession,
    user_id: str,
    include_expired: bool = False,
) -> List[Session]:
    """
    Get all sessions for a user.

    Args:
        db: Database session.
        user_id: ID of the user.
        include_expired: Whether to include expired sessions.

    Returns:
        List of Session objects for the user.
    """
    query = select(Session).where(Session.user_id == user_id)

    if not include_expired:
        now = datetime.now(timezone.utc)
        query = query.where(Session.expires_at > now)

    query = query.order_by(Session.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_session_by_id(
    db: AsyncSession,
    session_id: str,
) -> Optional[Session]:
    """
    Get a session by its ID.

    Args:
        db: Database session.
        session_id: ID of the session.

    Returns:
        Session if found, None otherwise.
    """
    result = await db.execute(
        select(Session).where(Session.id == session_id)
    )
    return result.scalar_one_or_none()


async def get_session_by_token(
    db: AsyncSession,
    token: str,
) -> Optional[Session]:
    """
    Get a session by its token.

    Args:
        db: Database session.
        token: Session token.

    Returns:
        Session if found, None otherwise.
    """
    result = await db.execute(
        select(Session).where(Session.token == token)
    )
    return result.scalar_one_or_none()


async def revoke_session(
    db: AsyncSession,
    session_id: str,
    user_id: str,
) -> bool:
    """
    Revoke (delete) a specific session.

    Args:
        db: Database session.
        session_id: ID of the session to revoke.
        user_id: ID of the user (for authorization check).

    Returns:
        True if session was revoked, False if not found.
    """
    result = await db.execute(
        delete(Session)
        .where(Session.id == session_id)
        .where(Session.user_id == user_id)
    )
    await db.commit()
    return result.rowcount > 0


async def revoke_all_sessions(
    db: AsyncSession,
    user_id: str,
    except_session_id: Optional[str] = None,
) -> int:
    """
    Revoke all sessions for a user.

    Args:
        db: Database session.
        user_id: ID of the user.
        except_session_id: Optional session ID to keep (e.g., current session).

    Returns:
        Number of sessions revoked.
    """
    query = delete(Session).where(Session.user_id == user_id)

    if except_session_id:
        query = query.where(Session.id != except_session_id)

    result = await db.execute(query)
    await db.commit()
    return result.rowcount


async def count_active_sessions(
    db: AsyncSession,
    user_id: str,
) -> int:
    """
    Count active (non-expired) sessions for a user.

    Args:
        db: Database session.
        user_id: ID of the user.

    Returns:
        Number of active sessions.
    """
    from sqlalchemy import func

    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(func.count())
        .select_from(Session)
        .where(Session.user_id == user_id)
        .where(Session.expires_at > now)
    )
    return result.scalar() or 0
