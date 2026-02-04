"""
Authentication Service

JWT verification via Better-Auth JWKS endpoint with caching.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import httpx
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError

from app.config import settings

logger = logging.getLogger(__name__)


class JWKSClient:
    """
    JWKS Client for fetching and caching public keys from Better-Auth.

    Implements key caching to reduce latency and network calls.
    """

    def __init__(
        self,
        jwks_url: Optional[str] = None,
        cache_ttl_seconds: int = 3600,
    ) -> None:
        """
        Initialize JWKS client.

        Args:
            jwks_url: URL to fetch JWKS from. Defaults to Better-Auth endpoint.
            cache_ttl_seconds: How long to cache JWKS keys (default 1 hour).
        """
        self.jwks_url = jwks_url or settings.jwks_url
        self.cache_ttl = timedelta(seconds=cache_ttl_seconds)
        self._jwks_cache: Optional[dict[str, Any]] = None
        self._cache_expiry: Optional[datetime] = None

    async def get_jwks(self) -> dict[str, Any]:
        """
        Fetch JWKS from Better-Auth with caching.

        Returns:
            JWKS dictionary containing public keys.

        Raises:
            httpx.HTTPError: If JWKS fetch fails.
        """
        now = datetime.now(timezone.utc)

        # Return cached JWKS if still valid
        if self._jwks_cache and self._cache_expiry and now < self._cache_expiry:
            return self._jwks_cache

        # Fetch fresh JWKS
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.jwks_url)
                response.raise_for_status()
                self._jwks_cache = response.json()
                self._cache_expiry = now + self.cache_ttl
                logger.info("JWKS cache refreshed from %s", self.jwks_url)
                return self._jwks_cache
        except httpx.HTTPError as e:
            logger.error("Failed to fetch JWKS: %s", str(e))
            # Return stale cache if available
            if self._jwks_cache:
                logger.warning("Using stale JWKS cache")
                return self._jwks_cache
            raise

    async def verify_token(self, token: str) -> dict[str, Any]:
        """
        Verify and decode a JWT token using JWKS.

        Args:
            token: JWT token string to verify.

        Returns:
            Decoded token payload.

        Raises:
            JWTError: If token verification fails.
        """
        try:
            jwks = await self.get_jwks()

            # Get the signing key from JWKS
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")

            signing_key = None
            for key in jwks.get("keys", []):
                if key.get("kid") == kid:
                    signing_key = key
                    break

            if not signing_key:
                # Fallback: try first key if no kid match
                keys = jwks.get("keys", [])
                if keys:
                    signing_key = keys[0]
                else:
                    raise JWTError("No signing keys found in JWKS")

            # Verify and decode token
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=[settings.JWT_ALGORITHM],
                issuer=settings.JWT_ISSUER,
                audience=settings.JWT_AUDIENCE,
                options={
                    "verify_aud": bool(settings.JWT_AUDIENCE),
                    "verify_iss": bool(settings.JWT_ISSUER),
                },
            )

            return payload

        except ExpiredSignatureError:
            logger.warning("Token has expired")
            raise JWTError("Token has expired")
        except JWTClaimsError as e:
            logger.warning("Token claims validation failed: %s", str(e))
            raise JWTError(f"Invalid token claims: {str(e)}")
        except JWTError as e:
            logger.warning("Token verification failed: %s", str(e))
            raise

    def clear_cache(self) -> None:
        """Clear the JWKS cache."""
        self._jwks_cache = None
        self._cache_expiry = None


class HMACAuthService:
    """
    HMAC-based JWT verification for shared secret authentication.

    Use this when Better-Auth is configured with HS256 algorithm.
    """

    def __init__(self, secret: Optional[str] = None) -> None:
        """
        Initialize HMAC auth service.

        Args:
            secret: JWT secret. Defaults to BETTER_AUTH_SECRET.
        """
        self.secret = secret or settings.BETTER_AUTH_SECRET or "dev-secret-change-in-production"

    async def verify_token(self, token: str) -> dict[str, Any]:
        """
        Verify and decode a JWT token using shared secret.

        Args:
            token: JWT token string to verify.

        Returns:
            Decoded token payload.

        Raises:
            JWTError: If token verification fails.
        """
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=["HS256"],
                options={
                    "verify_aud": False,
                    "verify_iss": False,
                },
            )
            return payload
        except ExpiredSignatureError:
            raise JWTError("Token has expired")
        except JWTError as e:
            logger.warning("HMAC token verification failed: %s", str(e))
            raise


# Global JWKS client instance
jwks_client = JWKSClient()

# For HS256, use HMACAuthService instead
hmac_auth_service = HMACAuthService()


async def verify_jwt(token: str) -> dict[str, Any]:
    """
    Verify a JWT token using the configured method.

    Tries HS256 first (for locally issued tokens), then RS256 (JWKS).

    Args:
        token: JWT token string to verify.

    Returns:
        Decoded token payload.

    Raises:
        JWTError: If verification fails.
    """
    # Try HS256 first (for locally issued tokens)
    try:
        return await hmac_auth_service.verify_token(token)
    except JWTError:
        pass

    # Fall back to RS256 (JWKS) if HS256 fails
    if settings.JWT_ALGORITHM == "RS256":
        try:
            return await jwks_client.verify_token(token)
        except Exception as e:
            logger.warning("JWKS verification failed: %s", str(e))
            raise JWTError("Token verification failed")

    raise JWTError("Token verification failed")
