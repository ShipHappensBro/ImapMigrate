import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("./.env")


def get_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Environment variable {name!r} is not set")

    return value


LOG_DIR = Path("./logs/imapsync")
LOG_DIR.mkdir(parents=True, exist_ok=True)

SOURCE_SERVER = get_env("SOURCE_SERVER")
PORT_SOURCE = int(get_env("PORT_SOURCE"))
AUTH_USER_SOURCE = get_env("AUTH_USER_SOURCE")
PASSWORD_SOURCE = get_env("PASSWORD_SOURCE")

TARGET_SERVER = get_env("TARGET_SERVER")
PORT_TARGET = int(get_env("PORT_TARGET"))
AUTH_USER_TARGET = get_env("AUTH_USER_TARGET")
PASSWORD_TARGET = get_env("PASSWORD_TARGET")

__all__ = (
    "AUTH_USER_SOURCE",
    "AUTH_USER_TARGET",
    "LOG_DIR",
    "PASSWORD_SOURCE",
    "PASSWORD_TARGET",
    "PORT_SOURCE",
    "PORT_TARGET",
    "SOURCE_SERVER",
    "TARGET_SERVER",
)