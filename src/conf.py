from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    AliasChoices,
    Field,
    ImportString,
    PostgresDsn,
    RedisDsn,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="",
    )
    aws_secret_access_key: str = Field(
        default="",
        env="AWS_SECRET_ACCESS_KEY",
        description="AWS secret access key",
    )
    aws_access_key_id: str = Field(
        default="",
        env="AWS_ACCESS_KEY_ID",
        description="AWS access key ID",
    )
    aws_session_token: str = Field(
        default="",
        env="AWS_SESSION_TOKEN",
        description="AWS session token",
    )
    aws_region: str = Field(
        default="",
        env="AWS_REGION",
        description="AWS region",
    )
    endpoint_url: str | None = Field(
        default=None,
        env="ENDPOINT_URL",
        description="S3 endpoint URL",
    )
    database_url: str = Field(
        ..., env="DATABASE_URL", description="Postgres database URL"
    )


settings = Settings()
