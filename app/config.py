from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    coingecko_api_key: str = Field(alias="COINGECKO_API_KEY")

    postgres_host: str = Field(alias="POSTGRES_HOST")

    postgres_port: int = Field(alias="POSTGRES_PORT")

    postgres_db: str = Field(alias="POSTGRES_DB")

    postgres_user: str = Field(alias="POSTGRES_USER")

    postgres_password: str = Field(alias="POSTGRES_PASSWORD")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
