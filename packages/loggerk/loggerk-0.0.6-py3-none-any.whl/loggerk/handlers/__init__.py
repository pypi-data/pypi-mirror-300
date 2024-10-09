"""Handlers for the loggerk package."""
import logging
import logging.handlers
import os
from typing import Literal, Optional, Required, TypedDict

import httpx

from loggerk.formatters import Formatter

__all__ = [
    "BaseHandlerDictConfig",
    "FileHandlerDictConfig",
    "StreamHandlerDictConfig",
    "HTTPHandlerDictConfig",
    "HandlerDictConfig",
    "new_http_handler",
    "new_file_handler",
    "CustomHTTPHandler",
]

LoggingLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


BaseHandlerDictConfig = TypedDict(
    "BaseHandlerDictConfig",
    {
        "class": Required[
            Literal[
                "logging.FileHandler",
                "logging.StreamHandler",
                "logging.handlers.QueueHandler",
                "logging.handlers.MemoryHandler",
                "logging.handlers.SocketHandler",
                "logging.handlers.SysLogHandler",
                "logging.handlers.HTTPHandler",
                "logging.handlers.DatagramHandler",
                "logging.handlers.BufferingHandler",
                "logging.handlers.NTEventLogHandler",
                "logging.handlers.WatchedFileHandler",
                "logging.handlers.RotatingFileHandler",
                "logging.handlers.TimedRotatingFileHandler",
            ]
        ],
        "formatter": Required[Formatter],
        "level": Required[LoggingLevel],
    },
)
# class BaseHandlerDictConfig(TypedDict):
#     class_: Required[
#         Literal[
#             "logging.FileHandler",
#             "logging.StreamHandler",
#             "logging.handlers.QueueHandler",
#             "logging.handlers.MemoryHandler",
#             "logging.handlers.SocketHandler",
#             "logging.handlers.SysLogHandler",
#             "logging.handlers.HTTPHandler",
#             "logging.handlers.DatagramHandler",
#             "logging.handlers.BufferingHandler",
#             "logging.handlers.NTEventLogHandler",
#             "logging.handlers.WatchedFileHandler",
#             "logging.handlers.RotatingFileHandler",
#             "logging.handlers.TimedRotatingFileHandler",
#         ]
#     ]
#     formatter: Required[Formatter]
#     level: Required[LoggingLevel]


# FileHandlerDictConfig_ = TypedDict(
#     "FileHandlerDictConfig_",
#     {
#         "filename": Required[str],
#         "mode": Required[Literal["w", "a", "wb", "ab"]],
#         "maxBytes": int,
#         "backupCount": int,
#     },
# )

# class FileHandlerDictConfig(BaseHandlerDictConfig, FileHandlerDictConfig_, total=True):
#     """File handler configuration."""
#     pass

class FileHandlerDictConfig(BaseHandlerDictConfig, total=True):
    """File handler configuration."""
    filename: Required[str]
    mode: Required[Literal["w", "a", "wb", "ab"]]
    maxBytes: int
    backupCount: int


# StreamHandlerDictConfig_ = TypedDict(
#     "StreamHandlerDictConfig_",
#     {
#         "stream": Literal["ext://sys.stderr"],
#         "level": LoggingLevel,
#     },
# )

# class StreamHandlerDictConfig(BaseHandlerDictConfig, StreamHandlerDictConfig_, total=True):
#     """Stream handler configuration."""
#     pass

class StreamHandlerDictConfig(BaseHandlerDictConfig, total=True):
    """Stream handler configuration."""
    stream: Required[Literal["ext://sys.stderr"]]
    level: Required[LoggingLevel]


HTTPHandlerDictConfig = TypedDict(
    "HTTPHandlerDictConfig",
    {
        "class": "logging.handlers.HTTPHandler",
        "host": Required[str],
        "url": Required[str],
        "method": Required[Literal["GET", "POST"]],
        "secure": bool,
        "credentials": Required[str],
    },
)

# class HTTPHandlerDictConfig(BaseHandlerDictConfig, TypedDict, total=True):
#     class_: Literal["logging.handlers.HTTPHandler"] = "logging.handlers.HTTPHandler"
#     host: Required[str]
#     url: Required[str]
#     method: Required[Literal["GET", "POST"]]
#     secure: bool
#     credentials: Required[str]


HandlerDictConfig = (
    FileHandlerDictConfig | StreamHandlerDictConfig | HTTPHandlerDictConfig
)


def new_http_handler(
    *,
    host: str,
    url: str,
    method: Literal["GET", "POST"],
    secure: bool,
    credentials: str,
    formatter: Literal["simple", "complex"] = "simple",
    level: LoggingLevel = "DEBUG",
) -> HTTPHandlerDictConfig:
    """Create a new HTTP handler configuration."""
    return HTTPHandlerDictConfig(
        **{
            "class": "logging.handlers.HTTPHandler",
            "formatter": formatter,
            "level": level,
            "host": host,
            "url": url,
            "method": method,
            "secure": secure,
            "credentials": credentials,
        }
    )


def new_file_handler(
    filename: str,
    mode: Literal["w", "a", "wb", "ab"] = "w",
    max_bytes: int = 100000,
    backup_count: int = 10,
    level: LoggingLevel = "DEBUG",
    formatter: Literal["simple", "complex"] = "simple",
) -> FileHandlerDictConfig:
    """Create a new file handler configuration."""
    return FileHandlerDictConfig(
        **{
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": formatter,
            "level": level,
            "filename": filename,
            "mode": mode,
            "maxBytes": max_bytes,
            "backupCount": backup_count,
        }
    )


class CustomHTTPHandler(logging.Handler):
    """Custom HTTP handler for logging."""
    app_name: str

    def __init__(
        self,
        app_name: str,
        *,
        auth: Literal["Basic", "Bearer", None] = "Bearer",
        credentials: Optional[str] = None,
        urls: Optional[list[str]] = None,
        method: Literal["GET", "POST"] = "POST",
    ) -> None:
        self.app_name = app_name
        if urls is None:
            env_urls = os.getenv("LOGGER_URLS", "")
            self.urls = env_urls.split(",")
            if not self.urls:
                raise ValueError(
                    "URLs are required, either pass it as an argument or" + \
                    " set the LOGGER_URLS environment variable"
                )

        if auth:
            if credentials is None:
                credentials = os.getenv("LOGGER_CREDENTIALS")
                if not credentials:
                    raise ValueError(
                        "credentials is required, either pass it as an argument" + \
                        " or set the LOGGER_CREDENTIALS environment variable"
                    )
                credentials = f"{auth} {credentials}"

        self.credentials = credentials
        self.method = method
        super().__init__()

    def emit(self, record):
        log_entry = record.__dict__
        for url in self.urls:
            try:
                response = httpx.request(
                    method=self.method,
                    url=url,
                    params={
                        "microservice": self.app_name,
                    },
                    json=log_entry,
                    headers={
                        "Authorization": f"{self.credentials}",
                    },
                )
                if not response.is_success:
                    continue
                return
            except (
                httpx.TimeoutException,
                httpx.NetworkError,
            ) as _:
                continue

        # raise ConnectionError("Failed to send log entry to any of the URLs")
