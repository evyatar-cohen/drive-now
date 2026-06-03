from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./drive_now.db"
    redis_url: str = "redis://localhost:6379"
    log_file: str = "logs/drivenow.log"


settings = Settings()