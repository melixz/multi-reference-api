from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "multi-reference-api"
    debug: bool = False

    database_url: str = Field(..., validation_alias="DATABASE_URL")
    api_key: str = Field(..., validation_alias="API_KEY")
    api_key_header: str = Field("X-API-Key", validation_alias="API_KEY_HEADER")


settings = Settings()
