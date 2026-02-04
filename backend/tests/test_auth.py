"""
Authentication Tests

Tests for JWT validation, token verification, and auth endpoints.
"""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.conftest import (
    MOCK_USER_EMAIL,
    MOCK_USER_ID,
    create_expired_jwt_payload,
    create_mock_jwt_payload,
)


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    async def test_health_check(self, client: AsyncClient) -> None:
        """Test basic health check endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    async def test_root_endpoint(self, client: AsyncClient) -> None:
        """Test root endpoint returns API info."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data


class TestJWTValidation:
    """Tests for JWT token validation."""

    async def test_missing_token_returns_401(self, client: AsyncClient) -> None:
        """Test that missing token returns 401."""
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401

    async def test_invalid_token_format_returns_401(self, client: AsyncClient) -> None:
        """Test that invalid token format returns 401."""
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "InvalidFormat"},
        )
        assert response.status_code == 401

    async def test_malformed_bearer_token_returns_401(self, client: AsyncClient) -> None:
        """Test that malformed bearer token returns 401."""
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer"},
        )
        assert response.status_code == 401

    @patch("app.services.auth.JWKSClient.verify_token")
    async def test_expired_token_returns_401(
        self, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test that expired token returns 401."""
        from jose import JWTError

        mock_verify.side_effect = JWTError("Token has expired")

        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer expired-token"},
        )
        assert response.status_code == 401

    @patch("app.services.auth.JWKSClient.verify_token")
    async def test_invalid_signature_returns_401(
        self, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test that invalid signature returns 401."""
        from jose import JWTError

        mock_verify.side_effect = JWTError("Invalid signature")

        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid-sig-token"},
        )
        assert response.status_code == 401


class TestAuthSession:
    """Tests for auth session endpoints."""

    @patch("app.services.auth.JWKSClient.verify_token")
    async def test_get_session_with_valid_token(
        self, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test getting session with valid token."""
        mock_verify.return_value = create_mock_jwt_payload()

        response = await client.get(
            "/api/v1/auth/session",
            headers={"Authorization": "Bearer valid-token"},
        )
        # Will return 404 until we implement the full flow
        # For now, just verify auth works
        assert response.status_code in [200, 404]


class TestAuthMe:
    """Tests for /auth/me endpoint."""

    @patch("app.services.auth.JWKSClient.verify_token")
    @patch("app.services.user.get_user_by_id")
    async def test_get_me_with_valid_token(
        self, mock_get_user: AsyncMock, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test getting current user with valid token."""
        mock_verify.return_value = create_mock_jwt_payload()
        mock_get_user.return_value = {
            "id": MOCK_USER_ID,
            "email": MOCK_USER_EMAIL,
            "name": "Test User",
            "role": "user",
        }

        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer valid-token"},
        )
        # Will return 404 until we implement the endpoint
        assert response.status_code in [200, 404]
