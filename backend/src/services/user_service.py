from sqlmodel import Session, select
from typing import Optional, Tuple
import uuid
from datetime import datetime
from passlib.context import CryptContext
from src.models.user import User, UserCreate
from src.schemas.user import UserCreateRequest
from src.auth.jwt_handler import create_access_token


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    Service class for user-related operations.
    Handles user registration, authentication, and management.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        # Truncate password to 72 bytes to comply with bcrypt limitations
        if len(password.encode('utf-8')) > 72:
            password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')

        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Previously hashed password

        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        """
        Create a new user in the database.

        Args:
            session: Database session
            user_data: User creation data including email, password, etc.

        Returns:
            Created User object
        """
        # Check if user with email already exists
        existing_user = session.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            raise ValueError("User with this email already exists")

        # Validate password length before hashing (bcrypt limitation is 72 bytes)
        if len(user_data.password.encode('utf-8')) > 72:
            raise ValueError("Password must not exceed 72 bytes in length")

        # Hash the password
        hashed_password = UserService.hash_password(user_data.password)

        # Create the user object
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Add to session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            session: Database session
            email: User's email address
            password: User's plain text password

        Returns:
            User object if authentication successful, None otherwise
        """
        # Find user by email
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        # Check if user exists and password is correct
        if user and UserService.verify_password(password, user.hashed_password):
            return user

        return None

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email address.

        Args:
            session: Database session
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
        """
        Retrieve a user by user ID.

        Args:
            session: Database session
            user_id: User's UUID

        Returns:
            User object if found, None otherwise
        """
        user = session.exec(
            select(User).where(User.id == user_id)
        ).first()

        return user

    @staticmethod
    def generate_auth_token(user: User) -> str:
        """
        Generate a JWT token for the authenticated user.

        Args:
            user: User object to generate token for

        Returns:
            JWT token string
        """
        data = {
            "user_id": str(user.id),
            "email": user.email,
            "name": user.name
        }

        token = create_access_token(data=data)
        return token

    @staticmethod
    def update_user_password(session: Session, user_id: uuid.UUID, new_password: str) -> bool:
        """
        Update a user's password.

        Args:
            session: Database session
            user_id: ID of the user to update
            new_password: New plain text password

        Returns:
            True if successful, False otherwise
        """
        user = session.exec(
            select(User).where(User.id == user_id)
        ).first()

        if not user:
            return False

        # Hash the new password
        hashed_password = UserService.hash_password(new_password)
        user.hashed_password = hashed_password
        user.updated_at = datetime.utcnow()

        session.add(user)
        session.commit()
        session.refresh(user)

        return True