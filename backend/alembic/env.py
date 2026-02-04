"""
Alembic Environment Configuration

Async SQLAlchemy support for Neon PostgreSQL migrations.
"""

import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Add the backend directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Import models to register them with SQLAlchemy metadata
from app.models.base import Base
from app.models import User, Session, Account, Verification  # noqa: F401

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata from our models
target_metadata = Base.metadata

# Get database URL from environment or config
def get_url() -> str:
    """Get database URL, preferring sync URL for migrations."""
    # For migrations, use sync URL (without asyncpg)
    url = os.getenv("DATABASE_URL_SYNC")
    if url:
        return url

    # Fallback: convert async URL to sync
    async_url = os.getenv("DATABASE_URL", "")
    if async_url:
        return async_url.replace("postgresql+asyncpg://", "postgresql://")

    # Last resort: use alembic.ini setting
    return config.get_main_option("sqlalchemy.url", "")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with the provided connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in async mode using asyncpg."""
    # For async migrations, we need the async URL
    async_url = os.getenv("DATABASE_URL", "")
    if not async_url:
        sync_url = get_url()
        async_url = sync_url.replace("postgresql://", "postgresql+asyncpg://")

    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = async_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Supports both sync and async database connections.
    For Neon PostgreSQL, we use async by default.
    """
    # Check if we should use async
    use_async = os.getenv("ALEMBIC_USE_ASYNC", "false").lower() == "true"

    if use_async:
        asyncio.run(run_async_migrations())
    else:
        # Sync migration (default, more compatible)
        from sqlalchemy import engine_from_config

        configuration = config.get_section(config.config_ini_section) or {}
        configuration["sqlalchemy.url"] = get_url()

        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
