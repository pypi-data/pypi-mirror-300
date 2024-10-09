"""config module for loggerk package."""
import json
from typing import Any, Literal, TypedDict

from loggerk.formatters import BaseFormatter, Format, Formatter
from loggerk.handlers import (
    BaseHandlerDictConfig,
    FileHandlerDictConfig,
    HandlerDictConfig,
    HTTPHandlerDictConfig,
    StreamHandlerDictConfig,
)

__all__ = [
    "ConfigDict",
    "DEFAULT_CONFIG",
    "DEFAULT_DATE_FORMAT",
    "DEFAULT_SIMPLE_FORMATTER",
    "DEFAULT_COMPLEX_FORMATTER",
    "DEFAULT_FILE_HANDLER",
    "DEFAULT_STDOUT_HANDLER",
    "DEFAULT_HTTP_HANDLER",
    "DEFAULT_CONFIG",
    "RootLogger",
]


class RootLogger(TypedDict):
    """Root logger configuration."""
    handlers: list[str]
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


DEFAULT_FILE_HANDLER = FileHandlerDictConfig(**{
    "class": "logging.handlers.RotatingFileHandler",
    "formatter": "simple",
    "level": "DEBUG",
    "filename": "logs/app.log",
    "mode": "w",
    "maxBytes": 100000,
    "backupCount": 10,
}
)

DEFAULT_STDOUT_HANDLER = StreamHandlerDictConfig(**{
    "class": "logging.StreamHandler",
    "formatter": "simple",
    "level": "DEBUG",
}
)

DEFAULT_HTTP_HANDLER = HTTPHandlerDictConfig(**{
    "class": "loggerk.handlers.CustomHTTPHandler",
    "formatter": "complex",
    "level": "DEBUG",
    "method": "POST",
    "auth": "Bearer",
})


DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S %z"


DEFAULT_SIMPLE_FORMATTER = BaseFormatter(
    format="%(asctime)s [%(levelname)s] %(APP_NAME)s | %(name)s " + \
        "<Module: %(module)s> <File: %(pathname)s:%(lineno)d> \t %(message)s",
    datefmt=DEFAULT_DATE_FORMAT,
)

DEFAULT_COMPLEX_FORMATTER = BaseFormatter(
    format=json.dumps(
        Format(
            time="%(asctime)s",
            service="%(APP_NAME)%",
            logger="%(name)s",
            logLevel="%(levelname)s",
            module="%(module)s",
            pathname="%(pathname)s",
            line="%(lineno)d",
            message="%(message)s",
        )
    ),
    datefmt=DEFAULT_DATE_FORMAT,
)


class ConfigDict(TypedDict):
    """Configuration dictionary for loggerk."""
    version: int
    formatters: dict[Formatter, BaseFormatter]
    handlers: dict[str, HandlerDictConfig]
    root: dict[str, Any]


DEFAULT_CONFIG = ConfigDict(
    version=1,
    formatters={
        "simple": DEFAULT_SIMPLE_FORMATTER,
        "complex": DEFAULT_COMPLEX_FORMATTER,
    },
    handlers={
        "file": DEFAULT_FILE_HANDLER,
        "stdout": DEFAULT_STDOUT_HANDLER,
        "http": DEFAULT_HTTP_HANDLER,
    },
    root=RootLogger(
        handlers=["file", "stdout", "http"],
        level="DEBUG",
    ),
)
