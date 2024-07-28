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

from src.config.settings import AppSettings, LogSettings


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
    return CORSConfig(allow_origins=cast("list[str]", app_settings.ALLOWED_CORS_ORIGINS))


def get_structlog_config(
    log_settings: LogSettings,
) -> StructlogConfig:
    return StructlogConfig(
        structlog_logging_config=StructLoggingConfig(
            log_exceptions="always",
            standard_lib_logging_config=LoggingConfig(
                handlers={},
                root={
                    "level": logging.getLevelName(log_settings.LEVEL),
                    "handlers": ["queue_listener"],
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
                        "handlers": ["queue_listener"],
                    },
                    "granian.access": {
                        "propagate": False,
                        "level": log_settings.GRANIAN_ACCESS_LEVEL,
                        "handlers": ["queue_listener"],
                    },
                    "granian.error": {
                        "propagate": False,
                        "level": log_settings.GRANIAN_ERROR_LEVEL,
                        "handlers": ["queue_listener"],
                    },
                    "saq": {
                        "propagate": False,
                        "level": log_settings.SAQ_LEVEL,
                        "handlers": ["queue_listener"],
                    },
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
                },
            ),
        ),
        middleware_logging_config=LoggingMiddlewareConfig(
            request_log_fields=["method", "path", "path_params", "query"],
            response_log_fields=["status_code"],
        ),
    )
