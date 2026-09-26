"""Core configuration using Pydantic Settings."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # MongoDB
    mongodb_uri: str
    mongodb_database: str = "portfolio_db"

    # JWT Authentication
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # CORS
    frontend_url: str = "http://localhost:3000"
    admin_url: str = "http://localhost:5173"

    @property
    def cors_origins(self) -> List[str]:
        """Return list of allowed CORS origins."""
        return [self.frontend_url, self.admin_url]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
