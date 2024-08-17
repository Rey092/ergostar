"""Plugins configuration file."""
import asyncio
import logging
import os
import re
from typing import cast

import structlog
from aiogram import Bot
from aiogram.utils.formatting import Code
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.config.response_cache import ResponseCacheConfig
from litestar.logging.config import LoggingConfig
from litestar.logging.config import StructLoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.plugins.structlog import StructlogConfig

from src.config.settings import AppSettings
from src.config.settings import LogSettings
import aiogram.utils.markdown as fmt


def get_cache_config() -> ResponseCacheConfig:
    """Get cache configuration."""
    return ResponseCacheConfig()


def get_compression_config() -> CompressionConfig:
    """Get compression configuration."""
    return CompressionConfig(backend="gzip", gzip_compress_level=9)


def get_csrf_config(app_settings: AppSettings) -> CSRFConfig:
    """Get CSRF configuration."""
    return CSRFConfig(
        secret=app_settings.SECRET_KEY,
        cookie_secure=app_settings.CSRF_COOKIE_SECURE,
        cookie_name=app_settings.CSRF_COOKIE_NAME,
    )


def get_cors_config(app_settings: AppSettings) -> CORSConfig:
    """Get CORS config."""
    return CORSConfig(
        allow_origins=cast("list[str]", app_settings.ALLOWED_CORS_ORIGINS),
    )


class MyHandler(logging.Handler):
    """
    Feeds all events back into structlog.
    """

    def __init__(self, project_name=None, *args, **kwargs):
        print(args, kwargs)
        super(MyHandler, self).__init__(*args, **kwargs)
        self._log = structlog.get_logger()
        self._bot = Bot(token="7255659065:AAG6hSFhpW7XVTdLFTTKyY1x1Wyctg7dJaE")
        self._project_name = "litestar"

    def emit(self, record: logging.LogRecord) -> None:
        print("HELLO WORLD")
        print('--------------------------')
        print(record.levelno)
        print('--------------------------')
        print(record.msg)
        print('--------------------------')
        print(record.name)
        loop = asyncio.get_event_loop()
        loop.create_task(self.sent_message(record.exc_text))

    async def sent_message(self, msg: str) -> None:
        text = (
            f"Проект: {self._project_name}, Контейнер: {os.environ.get('CONTAINER_NAME')}.\n"
            # fmt.hbold(f"URL: {settings.BACKEND_URL}, Version: {settings.TOML_PROJECT_VERSION}."),
            f"Хьюстон, у нас проблема! 🚀\n"
            "- - - - -\n\n"
            f"```python\n{msg}\n```"
        )
        text = re.sub(r'[_*[\]()~>#+\-=|{}.!]', lambda x: '\\' + x.group(), text)
        await self._bot.send_message(
            chat_id="480476538",
            text=text,
            parse_mode="MarkdownV2",
        )


def get_structlog_config(
    app_settings: AppSettings,
    log_settings: LogSettings,
) -> StructlogConfig:
    """Get structlog configuration."""
    return StructlogConfig(
        structlog_logging_config=StructLoggingConfig(
            log_exceptions="always",
            standard_lib_logging_config=LoggingConfig(
                handlers={
                    "telegram": {
                        "level": "ERROR",
                        "class": "src.config.litestar.MyHandler",
                        "project_name": "litestar!!!",
                    },
                },
                root={
                    "level": logging.getLevelName(log_settings.LEVEL),
                    "handlers": ["queue_listener", "telegram"],
                },
                loggers={
                    "uvicorn.access": {
                        "propagate": False,
                        "level": log_settings.UVICORN_ACCESS_LEVEL,
                        "handlers": ["queue_listener"],
                    },
                    "uvicorn.error": {
                        "propagate": False,
                        "level": log_settings.UVICORN_ERROR_LEVEL,
                        "handlers": ["queue_listener", "telegram"],
                    },
                    **(
                        {
                            "sqlalchemy.engine": {
                                "propagate": False,
                                "level": log_settings.SQLALCHEMY_LEVEL,
                                "handlers": ["queue_listener"],
                            },
                            "sqlalchemy.pool": {
                                "propagate": False,
                                "level": log_settings.SQLALCHEMY_LEVEL,
                                "handlers": ["queue_listener"],
                            },
                        }
                        if app_settings.DEBUG
                        else {}
                    ),
                },
            ),
        ),
        middleware_logging_config=LoggingMiddlewareConfig(
            request_log_fields=["method", "path", "path_params", "query"],
            response_log_fields=["status_code"],
        ),
    )
