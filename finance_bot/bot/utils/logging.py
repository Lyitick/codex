"""Logging utilities."""
import logging


def get_logger(name: str) -> logging.Logger:
    """Return configured logger.

    Args:
        name: Logger name.

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)
