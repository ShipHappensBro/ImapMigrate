from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ImapSettings(BaseModel):
    server: str
    port: int = 993
    auth_user: str
    password: SecretStr


class Settings(BaseSettings):
    source: ImapSettings
    target: ImapSettings
    log_dir: Path = Path("./logs/imapsync")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()  # pyright: ignore[reportCallIssue]
