"""Logging configuration for the project."""
import logging
from logging.config import dictConfig

from bot.config.settings import settings

LOG_DIR = settings.log_file.parent
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": settings.log_level,
            "formatter": "standard",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": settings.log_level,
            "formatter": "standard",
            "filename": str(settings.log_file),
            "encoding": "utf-8",
        },
    },
    "root": {
        "level": settings.log_level,
        "handlers": ["console", "file"],
    },
}


def setup_logging() -> None:
    """Apply logging configuration."""
    dictConfig(LOGGING_CONFIG)
    logging.getLogger(__name__).info("Logging configured")
