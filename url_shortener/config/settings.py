from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    allowed_hosts: str

    model_config = SettingsConfigDict(
        env_file="url_shortener/config/.env", env_file_encoding="utf-8"
    )


@lru_cache
def get_settings():
    return Settings()
