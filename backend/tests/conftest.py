"""
Pytest Configuration and Fixtures

Provides async test client, mock JWT, and test database fixtures.
"""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any, AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings
from app.database import get_db
from app.main import app
from app.models.base import Base


# Test database URL (use SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session_factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


# Mock JWT data
MOCK_USER_ID = "test-user-123"
MOCK_USER_EMAIL = "test@example.com"
MOCK_ADMIN_ID = "admin-user-456"
MOCK_ADMIN_EMAIL = "admin@example.com"


def create_mock_jwt_payload(
    user_id: str = MOCK_USER_ID,
    email: str = MOCK_USER_EMAIL,
    role: str = "user",
    exp_hours: int = 1,
) -> dict[str, Any]:
    """Create a mock JWT payload."""
    now = datetime.now(timezone.utc)
    return {
        "sub": user_id,
        "email": email,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=exp_hours)).timestamp()),
        "iss": "http://localhost:3000",
        "aud": "http://localhost:8000",
    }


def create_expired_jwt_payload(user_id: str = MOCK_USER_ID) -> dict[str, Any]:
    """Create an expired JWT payload."""
    now = datetime.now(timezone.utc)
    return {
        "sub": user_id,
        "email": MOCK_USER_EMAIL,
        "role": "user",
        "iat": int((now - timedelta(hours=2)).timestamp()),
        "exp": int((now - timedelta(hours=1)).timestamp()),
        "iss": "http://localhost:3000",
        "aud": "http://localhost:8000",
    }


@pytest.fixture
def mock_valid_token() -> str:
    """Return a mock valid JWT token string."""
    return "valid-jwt-token-for-testing"


@pytest.fixture
def mock_expired_token() -> str:
    """Return a mock expired JWT token string."""
    return "expired-jwt-token-for-testing"


@pytest.fixture
def mock_invalid_token() -> str:
    """Return a mock invalid JWT token string."""
    return "invalid-jwt-token-for-testing"


@pytest.fixture
def mock_jwt_payload() -> dict[str, Any]:
    """Return a mock JWT payload for a regular user."""
    return create_mock_jwt_payload()


@pytest.fixture
def mock_admin_jwt_payload() -> dict[str, Any]:
    """Return a mock JWT payload for an admin user."""
    return create_mock_jwt_payload(
        user_id=MOCK_ADMIN_ID,
        email=MOCK_ADMIN_EMAIL,
        role="admin",
    )


@pytest.fixture
def mock_auth_service():
    """Create a mock auth service for testing."""
    mock_service = MagicMock()
    mock_service.verify_token = AsyncMock(return_value=create_mock_jwt_payload())
    mock_service.get_jwks = AsyncMock(return_value={"keys": []})
    return mock_service
