from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"), env_file_encoding="utf-8", extra="ignore"
    )


class Config(CustomBaseSettings):

    EMAIL: str = Field(alias="AIRFLOW_EMAIL")

    LOG_FORMAT: str = (
        "[%(asctime)s] {%(filename)s:%(name)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    LOG_DATEFMT: str = "%Y-%m-%dT%H:%M:%SZ"
    LOG_LEVEL: str = Field(alias="LOG_LEVEL", default="INFO")


@lru_cache
def get_settings():
    return Config()  # type: ignore


settings = get_settings()
