import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("./.env")


def get_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Environment variable {name!r} is not set"
        )

    return value

LOG_DIR = Path("./logs/imapsync")
LOG_DIR.mkdir(parents=True, exist_ok=True)

HOST = get_env("HOST")
PORT = int(get_env("PORT"))

AUTH_USER = get_env("AUTH_USER")
TARGET_USER = get_env("TARGET_USER")
PASSWORD = get_env("PASSWORD")

HOST1 = get_env("HOST1")
AUTHUSER1 = get_env("AUTHUSER1")
PASSWORD1 = get_env("PASSWORD1")

HOST2 = get_env("HOST2")
AUTHUSER2 = get_env("AUTHUSER2")
PASSWORD2 = get_env("PASSWORD2")

USER1 = get_env("USER1")
USER2 = get_env("USER2")


__all__ = (
    "AUTHUSER1",
    "AUTHUSER2",
    "AUTH_USER",
    "HOST",
    "HOST1",
    "HOST2",
    "PASSWORD",
    "PASSWORD1",
    "PASSWORD2",
    "PORT",
    "TARGET_USER",
    "USER1",
    "USER2",
)