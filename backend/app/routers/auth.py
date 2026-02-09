"""
Authentication Router

Endpoints for signup, signin, JWT validation, session info, and current user profile.
"""

import hashlib
import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.account import Account
from app.models.session import Session
from app.models.user import User
from app.schemas.session import AccountRead, AccountsListResponse
from app.schemas.user import UserRead
from app.services import account as account_service
from app.utils.dependencies import (
    get_active_user,
    get_current_user,
    get_current_user_id,
    get_token_from_header,
)
from app.utils.exceptions import BadRequestError, NotFoundError

router = APIRouter(prefix="/auth", tags=["auth"])

# Bcrypt password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password using bcrypt via passlib."""
    return pwd_context.hash(password)


def _legacy_verify_sha256(password: str, hashed: str) -> bool:
    """Verify password against legacy SHA-256 hash (salt:hash format)."""
    try:
        salt, pwd_hash = hashed.split(":")
        return hashlib.sha256((password + salt).encode()).hexdigest() == pwd_hash
    except ValueError:
        return False


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash. Supports bcrypt and legacy SHA-256."""
    # Check if this is a bcrypt hash (starts with $2b$ or $2a$)
    if hashed.startswith(("$2b$", "$2a$")):
        return pwd_context.verify(password, hashed)
    # Legacy SHA-256 format: salt:hash
    return _legacy_verify_sha256(password, hashed)


def validate_password_strength(password: str) -> Optional[str]:
    """Validate password meets strength requirements. Returns error message or None."""
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least 1 uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Password must contain at least 1 lowercase letter"
    if not re.search(r"[0-9]", password):
        return "Password must contain at least 1 number"
    return None


def create_access_token(user_id: str, email: str, role: str = "user") -> tuple[str, datetime]:
    """Create JWT access token."""
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {
        "sub": user_id,
        "user_id": user_id,  # For frontend compatibility
        "email": email,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": expires_at,
    }
    secret = settings.BETTER_AUTH_SECRET
    if not secret:
        raise ValueError("BETTER_AUTH_SECRET must be set")
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token, expires_at


# Request/Response schemas for signup/signin
class SignUpRequest(BaseModel):
    """Signup request schema."""
    email: EmailStr
    password: str
    name: Optional[str] = None


class SignInRequest(BaseModel):
    """Signin request schema."""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Auth response with token."""
    success: bool = True
    data: dict


@router.post("/signup", response_model=AuthResponse)
async def signup(
    request: SignUpRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """
    Register a new user.

    Creates a new user account and returns a JWT token.
    """
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == request.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists",
        )

    # Validate password strength
    password_error = validate_password_strength(request.password)
    if password_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "Validation failed",
                "error_code": "VALIDATION_ERROR",
                "details": {"password": password_error},
            },
        )

    # Create user ID
    user_id = secrets.token_hex(16)

    # Create new user
    new_user = User(
        id=user_id,
        email=request.email,
        name=request.name,
        email_verified=False,
        role="user",
        banned=False,
    )
    db.add(new_user)

    # Create account with bcrypt-hashed password
    account = Account(
        id=secrets.token_hex(16),
        user_id=user_id,
        account_id=request.email,
        provider_id="credential",
        password=hash_password(request.password),
    )
    db.add(account)

    await db.commit()
    await db.refresh(new_user)

    # Create JWT token
    token, expires_at = create_access_token(user_id, request.email, "user")

    return AuthResponse(
        success=True,
        data={
            "token": token,
            "user_id": user_id,
            "expires_at": expires_at.isoformat(),
        },
    )


@router.post("/signin", response_model=AuthResponse)
async def signin(
    request: SignInRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """
    Sign in with email and password.

    Returns a JWT token for authenticated requests.
    """
    # Find user by email
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Check if user is banned
    if user.banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is banned",
        )

    # Find credential account
    result = await db.execute(
        select(Account)
        .where(Account.user_id == user.id)
        .where(Account.provider_id == "credential")
    )
    account = result.scalar_one_or_none()

    if not account or not account.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(request.password, account.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Transparent bcrypt migration: if legacy SHA-256, re-hash to bcrypt
    if not account.password.startswith(("$2b$", "$2a$")):
        account.password = hash_password(request.password)
        await db.flush()

    # Create JWT token
    token, expires_at = create_access_token(user.id, user.email, user.role)

    return AuthResponse(
        success=True,
        data={
            "token": token,
            "user_id": user.id,
            "expires_at": expires_at.isoformat(),
        },
    )


class SessionInfo(BaseModel):
    """Session information response."""

    session_id: str
    user_id: str
    expires_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_impersonated: bool = False


class SessionResponse(BaseModel):
    """Response with session and user data."""

    session: SessionInfo
    user: UserRead


class TokenInfo(BaseModel):
    """JWT token information."""

    user_id: str
    email: Optional[str] = None
    role: Optional[str] = None
    issued_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


@router.get("/session", response_model=SessionResponse)
async def get_session(
    user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token_from_header),
) -> SessionResponse:
    """
    Get current session and user information.

    Validates the JWT token and returns the associated session
    and user data from the database.

    Returns:
        SessionResponse with session and user details.

    Raises:
        401: If token is invalid or expired.
        403: If user is banned.
        404: If session not found in database.
    """
    # Find active session for this user
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(Session)
        .where(Session.user_id == user.id)
        .where(Session.expires_at > now)
        .order_by(Session.created_at.desc())
        .limit(1)
    )
    session = result.scalar_one_or_none()

    if not session:
        # Session might not exist in DB if using stateless JWT
        # Create a synthetic session info from the token
        from app.services.auth import verify_jwt

        payload = await verify_jwt(token)
        exp_timestamp = payload.get("exp", 0)

        return SessionResponse(
            session=SessionInfo(
                session_id="jwt-session",
                user_id=user.id,
                expires_at=datetime.fromtimestamp(exp_timestamp, tz=timezone.utc),
                is_impersonated=False,
            ),
            user=UserRead.model_validate(user),
        )

    return SessionResponse(
        session=SessionInfo(
            session_id=session.id,
            user_id=session.user_id,
            expires_at=session.expires_at,
            ip_address=session.ip_address,
            user_agent=session.user_agent,
            is_impersonated=session.is_impersonated,
        ),
        user=UserRead.model_validate(user),
    )


@router.get("/me", response_model=UserRead)
async def get_me(
    user: User = Depends(get_active_user),
) -> UserRead:
    """
    Get current authenticated user profile.

    Returns the full profile of the currently authenticated user.

    Returns:
        UserRead with user profile data.

    Raises:
        401: If token is invalid or expired.
        403: If user is banned.
    """
    return UserRead.model_validate(user)


@router.get("/token-info", response_model=TokenInfo)
async def get_token_info(
    token: str = Depends(get_token_from_header),
) -> TokenInfo:
    """
    Get information about the current JWT token.

    Decodes and returns the token payload without database lookup.
    Useful for debugging and token inspection.

    Returns:
        TokenInfo with decoded token data.

    Raises:
        401: If token is invalid or expired.
    """
    from app.services.auth import verify_jwt

    payload = await verify_jwt(token)

    iat_timestamp = payload.get("iat")
    exp_timestamp = payload.get("exp")

    return TokenInfo(
        user_id=payload.get("sub", ""),
        email=payload.get("email"),
        role=payload.get("role"),
        issued_at=(
            datetime.fromtimestamp(iat_timestamp, tz=timezone.utc)
            if iat_timestamp
            else None
        ),
        expires_at=(
            datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            if exp_timestamp
            else None
        ),
    )


@router.post("/verify")
async def verify_token(
    token: str = Depends(get_token_from_header),
) -> dict[str, Any]:
    """
    Verify that a token is valid.

    Simple endpoint to check token validity without fetching user data.

    Returns:
        Success message with user ID.

    Raises:
        401: If token is invalid or expired.
    """
    from app.services.auth import verify_jwt

    payload = await verify_jwt(token)

    return {
        "valid": True,
        "user_id": payload.get("sub"),
    }


@router.get("/accounts", response_model=AccountsListResponse)
async def get_my_accounts(
    user: User = Depends(get_active_user),
    db: AsyncSession = Depends(get_db),
) -> AccountsListResponse:
    """
    Get linked OAuth accounts for the current user.

    Returns:
        List of linked OAuth accounts.

    Raises:
        401: If token is invalid or expired.
        403: If user is banned.
    """
    accounts = await account_service.get_oauth_accounts(db, user.id)

    return AccountsListResponse(
        accounts=[AccountRead.model_validate(a) for a in accounts]
    )
