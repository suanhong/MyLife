from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MYLIFE_", env_file=".env", extra="ignore")

    environment: str = Field(default="development")
    project_id: str | None = Field(default=None)
    datastore_namespace: str | None = Field(default=None)
    storage_bucket: str | None = Field(default=None)


def get_settings() -> Settings:
    return Settings()
