"""Configuration for Music Player.

All secrets are read from environment variables (or a local .env file).
Never hard-code Telegram credentials in this file.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default=None):
    value = os.getenv(name)
    if value is None:
        return default
    value = value.strip()
    return value if value else default


def _bool_env(name: str, default: bool = False) -> bool:
    value = _env(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "y", "on"}


class Config:
    def __init__(self) -> None:
        api_id = _env("API_ID")
        api_hash = _env("API_HASH")
        session = _env("SESSION")

        if not api_id or not api_hash or not session:
            missing = [
                name for name, value in (
                    ("API_ID", api_id),
                    ("API_HASH", api_hash),
                    ("SESSION", session),
                ) if not value
            ]
            raise RuntimeError(
                "Missing required environment variable(s): " + ", ".join(missing)
            )

        try:
            self.API_ID: int = int(api_id)
        except ValueError as exc:
            raise RuntimeError("API_ID must be a numeric Telegram API ID.") from exc

        self.API_HASH: str = api_hash
        self.SESSION: str = session
        self.BOT_TOKEN: str | None = _env("BOT_TOKEN")

        sudoers_raw = _env("SUDOERS", "")
        self.SUDOERS: list[int] = []
        for user_id in sudoers_raw.replace(",", " ").split():
            try:
                self.SUDOERS.append(int(user_id))
            except ValueError:
                print(f"WARNING: Ignoring invalid SUDOERS value: {user_id!r}")

        self.SPOTIFY: bool = False
        self.QUALITY: str = (_env("QUALITY", "high") or "high").lower()
        self.PREFIXES: list[str] = (_env("PREFIX", "!") or "!").split()
        self.LANGUAGE: str = (_env("LANGUAGE", "en") or "en").lower()

        stream_mode = (_env("STREAM_MODE", "audio") or "audio").lower()
        self.STREAM_MODE: str = stream_mode if stream_mode in {"audio", "video"} else "audio"

        # Accept both the documented ADMINS_ONLY name and the old ADMIN_ONLY name.
        self.ADMINS_ONLY: bool = _bool_env(
            "ADMINS_ONLY", _bool_env("ADMIN_ONLY", False)
        )

        self.SPOTIFY_CLIENT_ID: str | None = _env("SPOTIFY_CLIENT_ID")
        self.SPOTIFY_CLIENT_SECRET: str | None = _env("SPOTIFY_CLIENT_SECRET")


config = Config()
