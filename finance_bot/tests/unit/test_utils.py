"""Tests for utility functions."""
from bot.utils.logging import get_logger


def test_get_logger_returns_logger() -> None:
    """get_logger should return a Logger instance with correct name."""
    logger = get_logger("test")
    assert logger.name == "test"
