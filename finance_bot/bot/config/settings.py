"""Application settings module."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / '.env')


@dataclass
class Settings:
    """Container for application settings."""

    bot_token: str
    database_url: str
    log_level: str = "INFO"
    log_file: Optional[Path] = BASE_DIR.parent / "logs" / "finance_bot.log"

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables.

        Returns:
            Settings: Loaded settings instance.
        """
        bot_token = os.getenv("BOT_TOKEN", "")
        database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./finance_bot.db")
        log_level = os.getenv("LOG_LEVEL", "INFO")
        log_file = os.getenv("LOG_FILE")
        log_file_path = Path(log_file) if log_file else BASE_DIR.parent / "logs" / "finance_bot.log"
        return cls(bot_token=bot_token, database_url=database_url, log_level=log_level, log_file=log_file_path)


settings = Settings.from_env()
