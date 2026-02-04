"""
Async Database Configuration

Provides async SQLAlchemy engine, session factory, and FastAPI dependency
for database session management.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import settings

# Create async engine with connection pooling
# Use NullPool for serverless environments like Neon PostgreSQL
# SQLite doesn't support pool_size/max_overflow
_db_url = settings.async_database_url
_is_sqlite = "sqlite" in _db_url

if _is_sqlite:
    engine = create_async_engine(
        _db_url,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_async_engine(
        _db_url,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=settings.DATABASE_POOL_SIZE if not settings.is_production else 0,
        max_overflow=settings.DATABASE_MAX_OVERFLOW if not settings.is_production else 0,
        poolclass=NullPool if settings.is_production else None,
    )

# Async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions.

    Yields an async database session and ensures proper cleanup.

    Usage:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions outside of FastAPI.

    Usage:
        async with get_db_context() as session:
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database connection and create tables if needed."""
    import logging
    logger = logging.getLogger(__name__)

    # Import models to ensure they're registered with SQLAlchemy
    from app.models.base import Base
    from app.models import User, Session, Account, Verification  # noqa: F401

    try:
        async with engine.begin() as conn:
            # Create tables if using SQLite (for local development)
            if "sqlite" in settings.async_database_url:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("SQLite tables created")
            else:
                # Test connection for PostgreSQL
                await conn.execute(text("SELECT 1"))
            logger.info("Database connection established")
    except Exception as e:
        logger.warning(f"Database connection failed: {e}. Server will start without database.")


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()
