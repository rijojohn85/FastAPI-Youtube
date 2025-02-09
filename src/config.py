import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DEV_DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".envrc",
        extra="ignore",
    )

Config = Settings()