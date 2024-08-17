"""Plugins configuration file."""

import logging
from typing import cast

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


def get_structlog_config(
    app_settings: AppSettings,
    log_settings: LogSettings,
) -> StructlogConfig:
    """Get structlog configuration."""
    handlers = ["queue_listener"]
    if log_settings.LOG_TELEGRAM_LOGGING_ENABLED:
        handlers.append("telegram")

    return StructlogConfig(
        structlog_logging_config=StructLoggingConfig(
            log_exceptions="always",
            standard_lib_logging_config=LoggingConfig(
                handlers={
                    "telegram": {
                        "level": "ERROR",
                        "class": "src.config.logging_handlers.telegram.TelegramHandler",
                        "project_name": "litestar!!!",
                        "backend_url": "http://localhost:8000",
                        "bot_token": log_settings.LOG_TELEGRAM_BOT_TOKEN,
                        "chat_id": log_settings.LOG_TELEGRAM_CHAT_ID,
                    }
                    if log_settings.LOG_TELEGRAM_LOGGING_ENABLED
                    else {},
                },
                root={
                    "level": logging.getLevelName(log_settings.LEVEL),
                    "handlers": handlers,
                },
                loggers={
                    "uvicorn.access": {
                        "propagate": False,
                        "level": log_settings.UVICORN_ACCESS_LEVEL,
                        "handlers": handlers,
                    },
                    "uvicorn.error": {
                        "propagate": False,
                        "level": log_settings.UVICORN_ERROR_LEVEL,
                        "handlers": handlers,
                    },
                    **(
                        {
                            "sqlalchemy.engine": {
                                "propagate": False,
                                "level": log_settings.SQLALCHEMY_LEVEL,
                                "handlers": handlers,
                            },
                            "sqlalchemy.pool": {
                                "propagate": False,
                                "level": log_settings.SQLALCHEMY_LEVEL,
                                "handlers": handlers,
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
