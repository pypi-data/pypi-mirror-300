"""Formatters module for loggerk package."""

from typing import Literal, TypedDict

Formatter = Literal["simple", "complex"]


__all__ = ["Formatter", "Format", "BaseFormatter"]


class Format(TypedDict, total=True):
    """Log record format."""

    time: str
    service: str
    logger: str
    logLevel: str
    module: str
    pathname: str
    line: int
    message: str


class BaseFormatter(TypedDict, total=True):
    """Base formatter for log records."""

    format: str
    datefmt: str
