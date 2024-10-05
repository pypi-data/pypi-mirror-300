import datetime
import logging
from pathlib import Path
import sys
from typing import Any, MutableMapping, Optional

from . import config

sys.stdout.reconfigure(line_buffering=False)  # type: ignore

Logger = logging.Logger | logging.LoggerAdapter


# Simple adapter that supports adding a single string-formattable object as context
class LogContextAdapter(logging.LoggerAdapter):
    def __init__(self, logger: Logger, context: Any):
        super().__init__(logger)
        self.context = context

    def process(self, msg, kwargs) -> tuple[Any, MutableMapping[str, Any]]:
        return (f"[{self.context}] {msg}", kwargs)  # type: ignore


def make_logger(name: str, stdout: bool, file: Optional[Path] = None) -> logging.Logger:
    logger = logging.getLogger(name)

    # Prevent duplicate initializations
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    if stdout:
        handler: logging.Handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)

    if file:
        config.log_dir.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(file)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    logger.debug(f"START {name} {datetime.datetime.today()}")

    return logger


# Default logger for this project
logger: Logger = make_logger("cctt", True, config.log_files["app"])
