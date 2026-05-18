import os
from dotenv import load_dotenv

load_dotenv()


def get_int_env(name: str, default: int | None = None) -> int | None:
    value = os.getenv(name)

    if value is None or value.strip() == "":
        return default

    try:
        return int(value)
    except ValueError:
        return default


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
    CHAT_ID = get_int_env("CHAT_ID")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = get_int_env("DB_PORT", 3306)
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "")