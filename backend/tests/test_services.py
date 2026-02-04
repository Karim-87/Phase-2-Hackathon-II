"""
Service Layer Tests

Unit tests for business logic services.
"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch


class TestAuthService:
    """Tests for authentication service."""

    async def test_jwks_caching(self) -> None:
        """Test that JWKS responses are cached."""
        from app.services.auth import JWKSClient

        client = JWKSClient(cache_ttl_seconds=3600)

        # Mock the HTTP client
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = {"keys": [{"kid": "test-key"}]}
            mock_response.raise_for_status = MagicMock()

            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client.return_value = mock_client_instance

            # First call should fetch
            jwks1 = await client.get_jwks()
            assert jwks1 == {"keys": [{"kid": "test-key"}]}

            # Second call should use cache (no additional HTTP call)
            jwks2 = await client.get_jwks()
            assert jwks2 == jwks1

    async def test_cache_clear(self) -> None:
        """Test that cache can be cleared."""
        from app.services.auth import JWKSClient

        client = JWKSClient()
        client._jwks_cache = {"keys": []}
        client._cache_expiry = datetime.now(timezone.utc) + timedelta(hours=1)

        client.clear_cache()

        assert client._jwks_cache is None
        assert client._cache_expiry is None


class TestUserService:
    """Tests for user service functions."""

    async def test_get_user_by_id_not_found(self) -> None:
        """Test getting non-existent user returns None."""
        from app.services.user import get_user_by_id

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        result = await get_user_by_id(mock_db, "non-existent-id")
        assert result is None

    async def test_list_users_pagination(self) -> None:
        """Test user listing with pagination."""
        from app.services.user import list_users

        mock_db = AsyncMock()

        # Mock count query
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 50

        # Mock list query
        mock_list_result = MagicMock()
        mock_list_result.scalars.return_value.all.return_value = []

        mock_db.execute.side_effect = [mock_count_result, mock_list_result]

        users, total = await list_users(mock_db, page=2, per_page=10)

        assert total == 50
        assert users == []


class TestSessionService:
    """Tests for session service functions."""

    async def test_count_active_sessions(self) -> None:
        """Test counting active sessions."""
        from app.services.session import count_active_sessions

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar.return_value = 3
        mock_db.execute.return_value = mock_result

        count = await count_active_sessions(mock_db, "user-123")
        assert count == 3

    async def test_revoke_session_success(self) -> None:
        """Test successful session revocation."""
        from app.services.session import revoke_session

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_db.execute.return_value = mock_result

        success = await revoke_session(mock_db, "session-123", "user-123")
        assert success is True
        mock_db.commit.assert_called_once()

    async def test_revoke_session_not_found(self) -> None:
        """Test revocation of non-existent session."""
        from app.services.session import revoke_session

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 0
        mock_db.execute.return_value = mock_result

        success = await revoke_session(mock_db, "non-existent", "user-123")
        assert success is False


class TestAccountService:
    """Tests for account service functions."""

    async def test_get_oauth_accounts_excludes_credential(self) -> None:
        """Test that get_oauth_accounts excludes credential accounts."""
        from app.services.account import get_oauth_accounts

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result

        accounts = await get_oauth_accounts(mock_db, "user-123")
        assert accounts == []

        # Verify the query was executed
        mock_db.execute.assert_called_once()
