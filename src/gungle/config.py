from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Gungle Backend"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./gungle.db"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB

    # Game Settings
    MAX_GUESSES: int = 5
    SESSION_TIMEOUT_HOURS: int = 24

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
