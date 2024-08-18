"""CORS config module."""

from typing import cast

from litestar.config.cors import CORSConfig

from src.config.settings import AppSettings


def get_cors_config(app_settings: AppSettings) -> CORSConfig:
    """Get CORS config."""
    return CORSConfig(
        allow_origins=cast("list[str]", app_settings.ALLOWED_CORS_ORIGINS),
    )
