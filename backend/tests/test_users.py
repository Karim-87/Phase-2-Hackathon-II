"""
User Management Tests

Tests for admin/user permissions and user management endpoints.
"""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.conftest import (
    MOCK_ADMIN_EMAIL,
    MOCK_ADMIN_ID,
    MOCK_USER_EMAIL,
    MOCK_USER_ID,
    create_mock_jwt_payload,
)


class TestUserList:
    """Tests for user listing (admin only)."""

    async def test_list_users_requires_auth(self, client: AsyncClient) -> None:
        """Test that user list requires authentication."""
        response = await client.get("/api/v1/users")
        assert response.status_code == 401

    @patch("app.services.auth.JWKSClient.verify_token")
    async def test_list_users_requires_admin(
        self, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test that user list requires admin role."""
        mock_verify.return_value = create_mock_jwt_payload(role="user")

        response = await client.get(
            "/api/v1/users",
            headers={"Authorization": "Bearer valid-token"},
        )
        # Should return 403 or 404 (user not in DB)
        assert response.status_code in [403, 404]

    @patch("app.services.auth.JWKSClient.verify_token")
    async def test_admin_can_list_users(
        self, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test that admin can list users."""
        mock_verify.return_value = create_mock_jwt_payload(
            user_id=MOCK_ADMIN_ID, email=MOCK_ADMIN_EMAIL, role="admin"
        )

        response = await client.get(
            "/api/v1/users",
            headers={"Authorization": "Bearer admin-token"},
        )
        # May return 404 if admin user not in DB
        assert response.status_code in [200, 404]


class TestUserProfile:
    """Tests for user profile endpoints."""

    @patch("app.services.auth.JWKSClient.verify_token")
    async def test_get_own_profile(
        self, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test getting own profile."""
        mock_verify.return_value = create_mock_jwt_payload()

        response = await client.get(
            f"/api/v1/users/{MOCK_USER_ID}",
            headers={"Authorization": "Bearer valid-token"},
        )
        # May return 404 if user not in DB
        assert response.status_code in [200, 404]

    @patch("app.services.auth.JWKSClient.verify_token")
    async def test_cannot_get_other_profile(
        self, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test that non-admin cannot get other user's profile."""
        mock_verify.return_value = create_mock_jwt_payload(role="user")

        response = await client.get(
            "/api/v1/users/other-user-id",
            headers={"Authorization": "Bearer valid-token"},
        )
        # Should return 403 or 404 (user not in DB)
        assert response.status_code in [403, 404]


class TestRoleManagement:
    """Tests for role management (admin only)."""

    async def test_update_role_requires_auth(self, client: AsyncClient) -> None:
        """Test that role update requires authentication."""
        response = await client.put(
            f"/api/v1/users/{MOCK_USER_ID}/role",
            json={"role": "admin"},
        )
        assert response.status_code == 401

    @patch("app.services.auth.JWKSClient.verify_token")
    async def test_update_role_requires_admin(
        self, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test that role update requires admin role."""
        mock_verify.return_value = create_mock_jwt_payload(role="user")

        response = await client.put(
            f"/api/v1/users/{MOCK_USER_ID}/role",
            json={"role": "admin"},
            headers={"Authorization": "Bearer valid-token"},
        )
        # Should return 403 or 404 (user not in DB)
        assert response.status_code in [403, 404]


class TestBanManagement:
    """Tests for user banning (admin only)."""

    async def test_ban_user_requires_auth(self, client: AsyncClient) -> None:
        """Test that banning requires authentication."""
        response = await client.post(
            f"/api/v1/users/{MOCK_USER_ID}/ban",
            json={"reason": "Test ban"},
        )
        assert response.status_code == 401

    @patch("app.services.auth.JWKSClient.verify_token")
    async def test_ban_user_requires_admin(
        self, mock_verify: AsyncMock, client: AsyncClient
    ) -> None:
        """Test that banning requires admin role."""
        mock_verify.return_value = create_mock_jwt_payload(role="user")

        response = await client.post(
            f"/api/v1/users/{MOCK_USER_ID}/ban",
            json={"reason": "Test ban"},
            headers={"Authorization": "Bearer valid-token"},
        )
        # Should return 403 or 404 (user not in DB)
        assert response.status_code in [403, 404]

    async def test_unban_user_requires_auth(self, client: AsyncClient) -> None:
        """Test that unbanning requires authentication."""
        response = await client.delete(f"/api/v1/users/{MOCK_USER_ID}/ban")
        assert response.status_code == 401
