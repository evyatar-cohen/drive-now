from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # if .env file is exist it override the defaults for local dev
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./drive_now.db"
    redis_url: str = "redis://localhost:6379"
    log_file: str = "logs/drivenow.log"


settings = Settings()