from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettingsWithConfigDict(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path("./app/.env"), extra="ignore")


class CORSSettings(BaseSettingsWithConfigDict):
    cors_origins: list[str] = ["*"]
    cors_credentials: bool = True
    cors_headers: list[str] = ["*"]
    cors_methods: list[str] = ["*"]


class DBSettings(BaseSettingsWithConfigDict):
    db_url: str
    db_echo: bool = False


class Settings(BaseSettingsWithConfigDict):
    db: DBSettings = DBSettings()  # type: ignore
    cors: CORSSettings = CORSSettings()


settings = Settings()

print(settings)
