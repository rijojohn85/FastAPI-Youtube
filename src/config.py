from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEV_DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(
        env_file=".envrc",
        extra="ignore",
    )


Config = Settings()
