import logging
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    bot_token: str = Field(..., alias="BOT_TOKEN")
    admin_ids: list[int] = Field(default_factory=list, alias="ADMIN_IDS")
    channel_jobs: str = Field(..., alias="CHANNEL_JOBS")
    channel_workers: str = Field(..., alias="CHANNEL_WORKERS")
    database_url: str = Field(..., alias="DATABASE_URL")
    moderation_enabled: bool = Field(True, alias="MODERATION_ENABLED")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""
    settings = Settings()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    return settings
