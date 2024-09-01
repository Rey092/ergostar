"""CSRF configuration module."""

from litestar.config.csrf import CSRFConfig

from src.main.config.settings import AppSettings


def get_csrf_config(app_settings: AppSettings) -> CSRFConfig:
    """Get CSRF configuration."""
    return CSRFConfig(
        secret=app_settings.SECRET_KEY,
        cookie_secure=app_settings.CSRF_COOKIE_SECURE,
        cookie_name=app_settings.CSRF_COOKIE_NAME,
    )
