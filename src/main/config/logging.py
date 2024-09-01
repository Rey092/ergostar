"""Plugins configuration file."""

import logging

from litestar.logging.config import LoggingConfig
from litestar.logging.config import StructLoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.plugins.structlog import StructlogConfig

from src.main.config.settings import AppSettings
from src.main.config.settings import LogSettings


def get_structlog_config(
    app_settings: AppSettings,
    log_settings: LogSettings,
) -> StructlogConfig:
    """Get structlog configuration."""
    handlers = ["queue_listener"]
    if log_settings.TELEGRAM_LOGGING_ENABLED:
        handlers.append("telegram")

    handlers_configs = {}
    if log_settings.TELEGRAM_LOGGING_ENABLED:
        handlers_configs["telegram"] = {
            "level": "ERROR",
            "class": "src.infrastructure.logging_handlers.telegram.TelegramHandler",
            "project_name": app_settings.PROJECT_NAME,
            "backend_url": app_settings.API_URL,
            "bot_token": log_settings.TELEGRAM_BOT_TOKEN,
            "chat_id": log_settings.TELEGRAM_CHAT_ID,
            "container_name": app_settings.CONTAINER_NAME,
        }

    return StructlogConfig(
        structlog_logging_config=StructLoggingConfig(
            log_exceptions="always",
            standard_lib_logging_config=LoggingConfig(
                handlers=handlers_configs,
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
                    "faststream": {
                        "propagate": False,
                        "level": log_settings.LEVEL,
                        "handlers": handlers,
                    },
                    "faststream.access": {
                        "propagate": False,
                        "level": log_settings.LEVEL,
                        "handlers": handlers,
                    },
                    "aiogram": {
                        "propagate": False,
                        "level": log_settings.LEVEL,
                        "handlers": handlers,
                    },
                    "aiogram.dispatcher": {
                        "propagate": False,
                        "level": log_settings.LEVEL,
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
