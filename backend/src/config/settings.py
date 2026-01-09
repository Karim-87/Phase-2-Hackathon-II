from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Database settings
    NEON_DATABASE_URL: str = os.getenv("NEON_DATABASE_URL", "")

    # Authentication settings
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_DELTA_HOURS: int = int(os.getenv("JWT_EXPIRATION_DELTA_HOURS", "24"))

    # Application settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

    # API settings
    API_V1_STR: str = "/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()