from functools import lru_cache
from typing import Optional
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

    vault_addr: str = Field(alias="VAULT_ADDR", default="http://127.0.0.1:8200")
    vault_approle: str = Field(alias="VAULT_APPROLE", default="airflow-approle")
    vault_secret_id: Optional[str] = Field(alias="VAULT_SECRET_ID")
    GRAFANA_LOKI_HOST: str = Field(alias="GRAFANA_LOKI_HOST")


@lru_cache
def get_settings():
    return Config()  # type: ignore


settings = get_settings()
