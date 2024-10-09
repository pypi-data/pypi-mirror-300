"""LoggerK is a singleton logger class that allows for easy logging configuration and management."""

import copy
import importlib
import logging
import os
from pathlib import Path
from typing import Literal, Optional, cast

from loggerk.config import DEFAULT_CONFIG, ConfigDict
from loggerk.formatters import BaseFormatter, Formatter
from loggerk.handlers import (
    BaseHandlerDictConfig,
    CustomHTTPHandler,
    FileHandlerDictConfig,
)

__all__ = ["LoggerK"]


class LoggerK(logging.Logger):
    """
    A singleton logger class that allows for easy logging configuration and management.
    """

    _instances: dict[str, "LoggerK"] = {}
    DEFAULT_CONFIG: ConfigDict = DEFAULT_CONFIG
    _file_path: str | None = None

    def __new__(
        cls,
        name: str,
        *args,
        **kwargs,
    ) -> "LoggerK":
        if not name in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]

    def __init__(
        self,
        name: str,
        config: Optional[ConfigDict] = None,
        app_name: Optional[str] = None,
        level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG",
        file_path: Optional[str] = None,
    ) -> None:
        """
        Initialize a LoggerK instance.

        Args:
            name (str): The name of the logger.
            app_name (str, optional): The name of the application. If not provided,
                it will be retrieved from the LOGGER_APP_NAME environment variable.
            level (LoggingLevel, optional): The logging level. Defaults to "DEBUG".
            config (Config, optional): The logger configuration. Defaults to DEFAULT_CONFIG.
            file_path (str, optional): The file path for log files. Defaults to None.
                Will be ignored if config does not have a file handler.
                If provided, it will override the filename in the file handler.

        Raises:
            ValueError: If app_name is not provided as an argument and LOGGER_APP_NAME
                environment variable is not set.
        """
        if app_name is None:

            app_name = os.getenv("LOGGER_APP_NAME")
            if not app_name:
                raise ValueError(
                    "app_name is required, either pass it as an argument or set"
                    + " the LOGGER_APP_NAME environment variable"
                )

        if config is None:
            config = copy.deepcopy(self.__class__.DEFAULT_CONFIG)

        super().__init__(name, level=level)

        if file_path:
            self._file_path = file_path
            self._assert_file_path(file_path)
        self._prepare_handlers(config)
        self._config = config

        self.app_name = app_name
        self._set_up_handlers()

    @property
    def config(self) -> ConfigDict:
        """returns a copy of the logger configuration."""
        return copy.deepcopy(self._config)

    @config.setter
    def config(self, new_config: ConfigDict):
        self._prepare_handlers(new_config)
        self._config = new_config
        self._set_up_handlers()

    def _set_up_handlers(self):
        self.handlers = []
        formatters: dict[Formatter, BaseFormatter] = self.config.get("formatters", {})
        for handler_config in self.config.get("handlers", {}).values():
            self._set_up_handler(
                handler_config=handler_config,
                formatters=formatters,
            )

    def _set_up_handler(
        self,
        handler_config: BaseHandlerDictConfig,
        formatters: dict[Formatter, BaseFormatter],
    ):

        class_: str = handler_config.get("class")
        module_str = ".".join(class_.split(".")[:-1])
        module = importlib.import_module(module_str)
        cls_name = handler_config.get("class").split(".")[-1]
        cls = getattr(module, cls_name)

        is_file_handler = (
            issubclass(cls, logging.handlers.RotatingFileHandler)
            or issubclass(cls, logging.FileHandler)
            or issubclass(cls, logging.handlers.TimedRotatingFileHandler)
        )
        if is_file_handler:
            handler_config = cast(FileHandlerDictConfig, handler_config)

            if self._file_path is not None:
                handler_config["filename"] = self._file_path

        if cls is CustomHTTPHandler:
            handler_config["app_name"] = self.app_name

        handler_config_copy = handler_config.copy()
        handler_config_copy.pop("class")
        handler_formatter = handler_config_copy.pop("formatter")
        handler_level = handler_config_copy.pop("level", self.level)
        handler: logging.Handler = cls(**handler_config_copy)

        handler.setLevel(handler_level)

        formatter_dict = formatters.get(handler_formatter)
        if formatter_dict:
            formatter = logging.Formatter(
                fmt=formatter_dict.get("format"),
                datefmt=formatter_dict.get("datefmt"),
            )
            handler.setFormatter(formatter)
        self.addHandler(handler)

    def _prepare_handlers(self, config: ConfigDict):
        for handler in config.get("handlers", {}).values():

            filename = self._file_path or handler.get("filename")
            if filename:
                self._assert_file_path(filename)

    def _assert_file_path(self, file_path: str):
        filename_path = Path(file_path)
        if filename_path.exists():
            return

        if filename_path.is_dir():
            log_dir = Path(filename_path)
            filename_path = Path(filename_path, f"{self.name}.log")
        else:
            log_dir = filename_path.parent

        if log_dir and not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        if not filename_path.exists():
            filename_path.touch()

    def filter(self, record: logging.LogRecord) -> bool:
        record.APP_NAME = self.app_name
        return super().filter(record)
