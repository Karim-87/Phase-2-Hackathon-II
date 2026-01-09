from sqlmodel import create_engine, Session
from typing import Generator
from src.config.settings import settings

# Create database engine
engine = create_engine(
    settings.NEON_DATABASE_URL,
    echo=(settings.ENVIRONMENT == "development"),  # Log SQL in development
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,   # Recycle connections every 5 minutes
)

def get_session() -> Generator[Session, None, None]:
    """
    Get database session for dependency injection.

    Yields:
        Session: Database session for the request
    """
    with Session(engine) as session:
        yield session