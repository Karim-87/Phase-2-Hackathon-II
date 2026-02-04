from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
import uuid

from src.database.session import get_session
from src.auth.dependencies import get_current_user
from src.services.user_service import UserService
from src.models.user import UserCreate
from src.schemas.user import (
    UserCreateRequest,
    UserLoginRequest,
    UserLoginResponse,
    UserResponse,
    UserData
)

router = APIRouter()


@router.post("/auth/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(
    user_request: UserCreateRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.
    """
    try:
        # Prepare user data
        user_data = UserCreate(
            email=user_request.email,
            password=user_request.password,
            name=user_request.name
        )

        # Create user in database
        db_user = UserService.create_user(session, user_data)

        # Generate authentication token
        token = UserService.generate_auth_token(db_user)

        # Prepare response data
        user_response_data = UserData(
            user_id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            token=token
        )

        return UserResponse(
            success=True,
            data=user_response_data
        )

    except ValueError as e:
        # Handle user already exists error
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        # Handle other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/auth/signin", response_model=UserLoginResponse)
def signin(
    login_request: UserLoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate an existing user and return JWT token.
    """
    try:
        # Authenticate user
        user = UserService.authenticate_user(
            session,
            login_request.email,
            login_request.password
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Generate authentication token
        token = UserService.generate_auth_token(user)

        # Prepare response data
        user_data = UserData(
            user_id=user.id,
            email=user.email,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            token=token
        )

        return UserLoginResponse(
            success=True,
            data=user_data
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )


@router.post("/auth/signout")
def signout():
    """
    Invalidate the user's session (client-side only).
    """
    return {"success": True, "message": "Successfully signed out"}


@router.get("/auth/me", response_model=UserResponse)
def get_current_user_profile(
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve current user's profile information.
    """
    # Get the user from the database using the authenticated user ID
    user = UserService.get_user_by_id(session, current_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prepare response data
    user_data = UserData(
        user_id=user.id,
        email=user.email,
        name=user.name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    return UserResponse(
        success=True,
        data=user_data
    )