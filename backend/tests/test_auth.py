"""
Authentication Tests

Tests for signup, signin, JWT validation, password hashing, and auth endpoints.
Uses async fixtures from conftest.py with SQLite test database.
"""

import hashlib
import secrets

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import create_test_token, create_test_user


class TestSignUp:
    """Tests for POST /api/v1/auth/signup."""

    @pytest.mark.asyncio
    async def test_signup_valid_data(self, client: AsyncClient) -> None:
        """Signup with valid data returns 200 and token."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "StrongPass1",
                "name": "New User",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "token" in data["data"]
        assert "user_id" in data["data"]
        assert "expires_at" in data["data"]

    @pytest.mark.asyncio
    async def test_signup_duplicate_email(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Signup with duplicate email returns 400."""
        await create_test_user(db_session, email="dupe@example.com")

        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "dupe@example.com",
                "password": "StrongPass1",
                "name": "Duplicate",
            },
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_signup_weak_password_no_uppercase(self, client: AsyncClient) -> None:
        """Signup with password missing uppercase returns 422."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "weak@example.com",
                "password": "weakpass1",
                "name": "Weak",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_signup_short_password(self, client: AsyncClient) -> None:
        """Signup with password < 8 chars returns 422."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "short@example.com",
                "password": "Sh1",
                "name": "Short",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_signup_password_no_number(self, client: AsyncClient) -> None:
        """Signup with password missing number returns 422."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "nonum@example.com",
                "password": "NoNumberHere",
                "name": "NoNum",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_signup_password_no_lowercase(self, client: AsyncClient) -> None:
        """Signup with password missing lowercase returns 422."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "nolower@example.com",
                "password": "NOLOWER123",
                "name": "NoLower",
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_signup_bcrypt_hash_format(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Signup stores password as bcrypt hash (starts with $2b$)."""
        from sqlalchemy import select

        from app.models.account import Account

        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "bcrypt@example.com",
                "password": "BcryptTest1",
                "name": "Bcrypt User",
            },
        )
        assert response.status_code == 200
        user_id = response.json()["data"]["user_id"]

        result = await db_session.execute(
            select(Account).where(Account.user_id == user_id)
        )
        account = result.scalar_one_or_none()
        assert account is not None
        assert account.password.startswith("$2b$")


class TestSignIn:
    """Tests for POST /api/v1/auth/signin."""

    @pytest.mark.asyncio
    async def test_signin_valid_credentials(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Signin with valid credentials returns 200 and token."""
        await create_test_user(db_session, email="signin@example.com")

        response = await client.post(
            "/api/v1/auth/signin",
            json={"email": "signin@example.com", "password": "TestPass1"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "token" in data["data"]

    @pytest.mark.asyncio
    async def test_signin_wrong_password(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Signin with wrong password returns 401."""
        await create_test_user(db_session, email="wrong@example.com")

        response = await client.post(
            "/api/v1/auth/signin",
            json={"email": "wrong@example.com", "password": "WrongPass1"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_signin_nonexistent_email(self, client: AsyncClient) -> None:
        """Signin with nonexistent email returns 401 (same message as wrong password)."""
        response = await client.post(
            "/api/v1/auth/signin",
            json={"email": "nobody@example.com", "password": "TestPass1"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_signin_legacy_sha256_migration(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Signin with legacy SHA-256 hash migrates to bcrypt."""
        from sqlalchemy import select

        from app.models.account import Account

        # Create a user with legacy SHA-256 hash
        password = "TestPass1"
        salt = secrets.token_hex(16)
        legacy_hash = salt + ":" + hashlib.sha256((password + salt).encode()).hexdigest()

        user_id, _ = await create_test_user(
            db_session,
            email="legacy@example.com",
            password_hash=legacy_hash,
        )

        # Sign in — should succeed and migrate hash
        response = await client.post(
            "/api/v1/auth/signin",
            json={"email": "legacy@example.com", "password": password},
        )
        assert response.status_code == 200

        # Verify the hash was migrated to bcrypt
        db_session.expire_all()
        result = await db_session.execute(
            select(Account).where(Account.user_id == user_id)
        )
        account = result.scalar_one_or_none()
        assert account is not None
        assert account.password.startswith(("$2b$", "$2a$"))


class TestAuthMe:
    """Tests for GET /api/v1/auth/me."""

    @pytest.mark.asyncio
    async def test_get_me_with_valid_token(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """GET /auth/me with valid token returns user profile."""
        user_id, token = await create_test_user(db_session, email="me@example.com")

        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "me@example.com"
        assert data["id"] == user_id

    @pytest.mark.asyncio
    async def test_get_me_without_token(self, client: AsyncClient) -> None:
        """GET /auth/me without token returns 401."""
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me_with_invalid_token(self, client: AsyncClient) -> None:
        """GET /auth/me with invalid token returns 401."""
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid-token-here"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me_malformed_header(self, client: AsyncClient) -> None:
        """GET /auth/me with malformed Authorization header returns 401."""
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "NotBearer token"},
        )
        assert response.status_code == 401


class TestTokenExpiration:
    """Tests for JWT token settings."""

    @pytest.mark.asyncio
    async def test_token_has_24h_expiration(
        self, db_session: AsyncSession
    ) -> None:
        """Token expiration is set to 24 hours from creation."""
        from datetime import datetime, timezone

        from app.routers.auth import create_access_token

        _, expires_at = create_access_token("test-user", "test@example.com")
        now = datetime.now(timezone.utc)
        diff_hours = (expires_at - now).total_seconds() / 3600
        # Should be approximately 24 hours (allow small delta for test execution time)
        assert 23.9 < diff_hours < 24.1


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient) -> None:
        """Test basic health check endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient) -> None:
        """Test root endpoint returns API info."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
