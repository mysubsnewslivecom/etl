from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional


def get_postgres_url() -> str:
    return f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"


def get_redis_url() -> str:
    return f"redis://:{settings.redis_password}@{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"


class Settings(BaseSettings, case_sensitive=True):
    # model_config = SettingsConfigDict(
    #     # env_nested_delimiter="__", env_file=".env", extra="ignore"
    #     # env_nested_delimiter="__",
    #     env_file=str(dotenv_path),
    #     extra="ignore",
    #     case_sensitive=False,
    # )

    log_level: str = Field(..., alias="LOG_LEVEL")
    # log_format: str = Field(..., alias="LOG_FORMAT")
    # log_date_format: str = Field(..., alias="LOG_DATE_FORMAT")
    postgres_user: Optional[str] = Field(..., alias="POSTGRES_USER")
    postgres_password: Optional[SecretStr] = Field(..., alias="POSTGRES_PASSWORD")
    postgres_host: Optional[str] = Field(..., alias="POSTGRES_HOST")
    postgres_port: Optional[int] = Field(..., alias="POSTGRES_PORT")
    postgres_db: Optional[str] = Field(..., alias="POSTGRES_DB")
    redis_host: Optional[str] = Field(..., alias="REDIS_HOST")
    redis_port: Optional[int] = Field(..., alias="REDIS_PORT")
    redis_db: Optional[int] = Field(..., alias="REDIS_DB")
    redis_password: Optional[SecretStr] = Field(..., alias="REDIS_PASSWORD")
    iss_location_api: Optional[str] = Field(..., alias="ISS_LOCATION_API")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
print(get_postgres_url())
