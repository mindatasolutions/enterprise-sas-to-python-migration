"""
Enterprise logging module.

Provides a reusable logger for all project modules.
"""

from pathlib import Path
import logging

from generator.config import Config


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Parameters
    ----------
    name : str
        Logger name.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    Config.LOGS.mkdir(parents=True, exist_ok=True)

    log_file = Path(Config.LOGS) / "migration.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    # Console
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # File
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger
