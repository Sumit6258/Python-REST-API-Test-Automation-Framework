"""
Centralised logging utility.

Usage:
    from utils.logger import get_logger
    log = get_logger(__name__)
    log.info("Starting test...")
"""

import logging
import sys
from pathlib import Path

try:
    import colorlog  # optional coloured console output
    _HAS_COLORLOG = True
except ImportError:
    _HAS_COLORLOG = False

from config.settings import settings

_LOGGERS: dict[str, logging.Logger] = {}


def _build_console_handler() -> logging.Handler:
    handler = logging.StreamHandler(sys.stdout)
    if _HAS_COLORLOG:
        fmt = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    else:
        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    handler.setFormatter(fmt)
    return handler


def _build_file_handler() -> logging.Handler:
    log_path = Path(settings.LOG_FILE_PATH)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(fmt)
    return handler


def get_logger(name: str) -> logging.Logger:
    """Return (and cache) a named logger configured for the framework."""
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(_build_console_handler())
        if settings.LOG_TO_FILE:
            logger.addHandler(_build_file_handler())

    _LOGGERS[name] = logger
    return logger
