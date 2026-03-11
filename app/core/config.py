from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Football Predictions API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./football_predictions.db"
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()