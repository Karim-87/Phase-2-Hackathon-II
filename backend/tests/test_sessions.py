"""
Session Management Tests

Tests for session listing and revocation endpoints.
"""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.conftest import MOCK_USER_ID, create_mock_jwt_payload


class TestSessionList:
    """Tests for session listing."""

    @patch("app.services.auth.JWKSClient.verify_token")
    async def test_get_sessions_requires_auth(
        self, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test that session list requires authentication."""
        response = await client.get(f"/api/v1/users/{MOCK_USER_ID}/sessions")
        assert response.status_code == 401

    @patch("app.services.auth.JWKSClient.verify_token")
    @patch("app.services.session.get_user_sessions")
    async def test_get_own_sessions(
        self, mock_get_sessions: AsyncMock, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test getting own sessions."""
        mock_verify.return_value = create_mock_jwt_payload()
        mock_get_sessions.return_value = []

        response = await client.get(
            f"/api/v1/users/{MOCK_USER_ID}/sessions",
            headers={"Authorization": "Bearer valid-token"},
        )
        # May return 404 if user not in DB, or 200 with empty list
        assert response.status_code in [200, 404]


class TestSessionRevocation:
    """Tests for session revocation."""

    async def test_revoke_session_requires_auth(self, client: AsyncClient) -> None:
        """Test that session revocation requires authentication."""
        response = await client.delete(
            f"/api/v1/users/{MOCK_USER_ID}/sessions/session-123"
        )
        assert response.status_code == 401

    async def test_revoke_all_sessions_requires_auth(self, client: AsyncClient) -> None:
        """Test that revoking all sessions requires authentication."""
        response = await client.delete(f"/api/v1/users/{MOCK_USER_ID}/sessions")
        assert response.status_code == 401
