from sqlmodel import create_engine, Session
from typing import Generator
from src.config.settings import settings

def get_database_url():
    """Get database URL with fallback to SQLite for local development."""
    url = settings.NEON_DATABASE_URL or settings.DATABASE_URL or getattr(settings, 'POSTGRES_URL', None)
    if not url or url == "postgresql://user:password@localhost:5432/todo_db":
        return "sqlite:///./app.db"  # SQLite for local development
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url

# Create database engine with fallback configuration
DATABASE_URL = get_database_url()

# Determine if using SQLite
_is_sqlite = "sqlite" in DATABASE_URL

if _is_sqlite:
    engine = create_engine(
        DATABASE_URL,
        echo=(settings.ENVIRONMENT == "development"),
        connect_args={"check_same_thread": False},  # Required for SQLite
    )
    # Import models and create tables for SQLite
    from src.models.task import Task  # noqa: F401
    from src.models.user import User  # noqa: F401
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
else:
    engine = create_engine(
        DATABASE_URL,
        echo=(settings.ENVIRONMENT == "development"),
        pool_pre_ping=True,
        pool_recycle=300,
    )

def get_session() -> Generator[Session, None, None]:
    """
    Get database session for dependency injection.

    Yields:
        Session: Database session for the request
    """
    with Session(engine) as session:
        yield session