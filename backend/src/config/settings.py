from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import json

class Settings(BaseSettings):
    # Database settings
    NEON_DATABASE_URL: str = os.getenv("NEON_DATABASE_URL", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_URL_UNPOOLED: str = os.getenv("DATABASE_URL_UNPOOLED", "")
    PGHOST: str = os.getenv("PGHOST", "")
    PGHOST_UNPOOLED: str = os.getenv("PGHOST_UNPOOLED", "")
    PGUSER: str = os.getenv("PGUSER", "")
    PGPASSWORD: str = os.getenv("PGPASSWORD", "")
    PGDATABASE: str = os.getenv("PGDATABASE", "")
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "")
    POSTGRES_URL_NON_POOLING: str = os.getenv("POSTGRES_URL_NON_POOLING", "")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE", "")
    POSTGRES_URL_NO_SSL: str = os.getenv("POSTGRES_URL_NO_SSL", "")
    POSTGRES_PRISMA_URL: str = os.getenv("POSTGRES_PRISMA_URL", "")

    # Stack/Authentication settings
    NEXT_PUBLIC_STACK_PROJECT_ID: str = os.getenv("NEXT_PUBLIC_STACK_PROJECT_ID", "")
    NEXT_PUBLIC_STACK_PUBLISHABLE_CLIENT_KEY: str = os.getenv("NEXT_PUBLIC_STACK_PUBLISHABLE_CLIENT_KEY", "")
    STACK_SECRET_SERVER_KEY: str = os.getenv("STACK_SECRET_SERVER_KEY", "")
    JWT: str = os.getenv("JWT", "")

    # Authentication settings
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_DELTA_HOURS: int = int(os.getenv("JWT_EXPIRATION_DELTA_HOURS", "24"))

    # Application settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # API settings
    API_V1_STR: str = "/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

    # Property for allowed origins
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        return [origin.strip() for origin in origins.split(",") if origin.strip()]


settings = Settings()