"""
Test Fixtures

Async SQLite engine, session factory, FastAPI TestClient with httpx.AsyncClient,
test user creation helper, JWT token generation helper.
"""

import secrets
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.database import get_db
from app.models.base import Base


# Test database engine (async SQLite)
test_engine = create_async_engine(
    "sqlite+aiosqlite:///./test.db",
    echo=False,
    connect_args={"check_same_thread": False},
)

TestSessionFactory = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Create all tables before each test and drop after."""
    from app.models import Account, Session, User, Verification  # noqa: F401
    from app.models.task import Task  # noqa: F401

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a test database session."""
    async with TestSessionFactory() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provide an async test client with overridden DB dependency."""
    from app.main import app

    async def override_get_db():
        try:
            yield db_session
            await db_session.commit()
        except Exception:
            await db_session.rollback()
            raise

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


def create_test_token(user_id: str, email: str = "test@example.com", role: str = "user") -> str:
    """Generate a JWT token for testing."""
    secret = settings.BETTER_AUTH_SECRET or "test-secret"
    payload = {
        "sub": user_id,
        "user_id": user_id,
        "email": email,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


async def create_test_user(
    db_session: AsyncSession,
    email: str = "test@example.com",
    name: str = "Test User",
    password_hash: str | None = None,
) -> tuple[str, str]:
    """
    Create a test user with account. Returns (user_id, token).

    If password_hash is None, creates a bcrypt hash of 'TestPass1'.
    """
    from passlib.context import CryptContext

    from app.models.account import Account
    from app.models.user import User

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    user_id = secrets.token_hex(16)
    user = User(
        id=user_id,
        email=email,
        name=name,
        email_verified=False,
        role="user",
        banned=False,
    )
    db_session.add(user)

    account = Account(
        id=secrets.token_hex(16),
        user_id=user_id,
        account_id=email,
        provider_id="credential",
        password=password_hash or pwd_context.hash("TestPass1"),
    )
    db_session.add(account)
    await db_session.commit()

    token = create_test_token(user_id, email)
    return user_id, token
