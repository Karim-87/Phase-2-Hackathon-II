"""
Application Configuration

Pydantic Settings for environment variable loading and validation.
Supports Better-Auth integration with JWT verification settings.
"""

import logging
import sys
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Database Configuration - supports multiple env var names
    DATABASE_URL: str = ""
    DATABASE_URL_SYNC: str = ""
    NEON_DATABASE_URL: str = ""
    POSTGRES_URL: str = ""

    @property
    def async_database_url(self) -> str:
        """Get async database URL, converting from sync if needed."""
        # Priority: DATABASE_URL > NEON_DATABASE_URL > POSTGRES_URL
        url = self.DATABASE_URL or self.NEON_DATABASE_URL or self.POSTGRES_URL
        if not url or url == "postgresql://user:password@localhost:5432/todo_db":
            # Use SQLite for local development if no real database configured
            return "sqlite+aiosqlite:///./app.db"
        # Convert to async driver if needed
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    @property
    def sync_database_url(self) -> str:
        """Get sync database URL for migrations."""
        url = self.DATABASE_URL_SYNC or self.NEON_DATABASE_URL or self.POSTGRES_URL or self.DATABASE_URL
        if not url:
            return "postgresql://localhost:5432/app"
        # Ensure it's sync driver
        return url.replace("postgresql+asyncpg://", "postgresql://", 1)
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Better-Auth Configuration
    BETTER_AUTH_URL: str = "http://localhost:3000"
    BETTER_AUTH_SECRET: str = ""

    # JWT Configuration
    JWT_ALGORITHM: str = "RS256"
    JWT_ISSUER: str = "http://localhost:3000"
    JWT_AUDIENCE: str = "http://localhost:8000"

    # Application Configuration
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # CORS Configuration
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse comma-separated ALLOWED_ORIGINS into a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT.lower() == "production"

    @property
    def jwks_url(self) -> str:
        """Get the JWKS endpoint URL from Better-Auth."""
        return f"{self.BETTER_AUTH_URL}/api/auth/jwks"


    def validate_production_config(self) -> None:
        """Validate configuration for production safety. Called on startup."""
        logger = logging.getLogger(__name__)

        if self.is_production:
            if not self.BETTER_AUTH_SECRET:
                raise ValueError(
                    "BETTER_AUTH_SECRET must be set in production environment"
                )
            # Warn if CORS origins contain localhost
            for origin in self.allowed_origins_list:
                if "localhost" in origin or "127.0.0.1" in origin:
                    logger.warning(
                        "Production CORS origin contains localhost: %s. "
                        "This is likely a misconfiguration.",
                        origin,
                    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()


def configure_logging() -> None:
    """Configure structured logging based on settings."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    if settings.LOG_FORMAT == "json":
        # JSON format for production
        log_format = (
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        # Human-readable format for development
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Set specific log levels for noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DEBUG else logging.WARNING
    )
