"""Base settings for the project."""

import binascii
import os
from pathlib import Path

from litestar.data_extractors import RequestExtractorField
from litestar.data_extractors import ResponseExtractorField
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

BASE_DIR: str = str(Path(__file__).parent.parent.parent)


class LiteStarSettings(BaseSettings):
    """Abstract settings."""

    """Model configuration."""
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )


class DatabaseSettings(LiteStarSettings):
    """Database settings."""

    """Model configuration."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="POSTGRES_",
        extra="ignore",
        env_file_encoding="utf-8",
    )

    """Database URL parts."""
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str | None = None
    PASSWORD: str | None = None
    DB: str | None = None

    @property
    def URL(self) -> str:
        """Database URL."""
        if all([self.USER, self.PASSWORD, self.DB]):
            return str(
                f"postgresql+asyncpg://"
                f"{self.USER}:"
                f"{self.PASSWORD}@"
                f"{self.HOST}:"
                f"{self.PORT}/"
                f"{self.DB}",
            )

        raise ValueError("Database URL is not set")

    """Enable SQLAlchemy engine logs."""
    ECHO: bool = False
    """Enable SQLAlchemy connection pool logs."""
    ECHO_POOL: bool = False
    """Disable SQLAlchemy pool configuration."""
    POOL_DISABLED: bool = False
    """Max overflow for SQLAlchemy connection pool"""
    POOL_MAX_OVERFLOW: int | bool = False
    """Pool size for SQLAlchemy connection pool"""
    POOL_SIZE: int = 5
    """Time in seconds for timing connections out of the connection pool."""
    POOL_TIMEOUT: int = 30
    """Amount of time to wait before recycling connections."""
    POOL_RECYCLE: int = 300
    """Optionally ping database before fetching a session from the connection pool."""
    POOL_PRE_PING: bool = False

    @property
    def migration_ddl_version_table(self) -> str:
        """The name to use for the `alembic` versions table name."""
        return "ddl_version"

    @property
    def migration_config(self) -> str:
        """The path to the `alembic.ini` configuration file."""
        return f"{BASE_DIR}/src/config/migrations/alembic.ini"

    @property
    def migration_path(self) -> str:
        """The path to the `alembic` database migrations."""
        return f"{BASE_DIR}/src/config/migrations"

    @property
    def fixture_path(self) -> str:
        """The path to JSON fixture files to load into tables."""
        return f"{BASE_DIR}/src/config/fixtures"


class LogSettings(LiteStarSettings):
    """Logger configuration."""

    """Regex to exclude paths from logging."""
    EXCLUDE_PATHS: str = r"\A(?!x)x"
    """Log event name for logs from Litestar handlers."""
    HTTP_EVENT: str = "HTTP"
    """Include 'body' of compressed responses in log output."""
    INCLUDE_COMPRESSED_BODY: bool = False
    """Stdlib log levels. Only emit logs at this level, or higher."""
    LEVEL: int = 10
    """Request cookie keys to obfuscate."""
    OBFUSCATE_COOKIES: set[str] = {"session"}
    """Request header keys to obfuscate."""
    OBFUSCATE_HEADERS: set[str] = {"Authorization", "X-API-KEY"}
    """Attributes of the [Request][litestar.connection.request.Request] to be logged."""
    REQUEST_FIELDS: list[RequestExtractorField] = [
        "path",
        "method",
        "headers",
        "cookies",
        "query",
        "path_params",
        "body",
    ]
    """Attributes of the [Response][litestar.response.Response] to be logged."""
    RESPONSE_FIELDS: list[ResponseExtractorField] = [
        "status_code",
        "cookies",
        "headers",
        "body",
    ]
    """Log event name for logs from SAQ worker."""
    WORKER_EVENT: str = "Worker"
    """Level to log SQLAlchemy logs."""
    SQLALCHEMY_LEVEL: int = 20
    """Level to log uvicorn access logs."""
    UVICORN_ACCESS_LEVEL: int = 20
    """Level to log uvicorn error logs."""
    UVICORN_ERROR_LEVEL: int = 20


class RedisSettings(LiteStarSettings):
    """Redis settings."""

    """A Redis connection URL."""
    URL: str = "redis://localhost:6379/0"
    """Length of time to wait (in seconds) for a connection to become active."""
    SOCKET_CONNECT_TIMEOUT: int = 5
    """Length of time to wait (in seconds) before testing connection health."""
    HEALTH_CHECK_INTERVAL: int = 5
    """Length of time to wait (in seconds) between keepalive commands."""
    SOCKET_KEEPALIVE: bool = True

    """Redis cache status."""
    CACHE_ENABLED: bool = True


class AppSettings(LiteStarSettings):
    """Application configuration."""

    """The frontend base URL"""
    URL: str = "http://localhost:8000"
    """Run `Litestar` with `debug=True`."""
    DEBUG: bool = True
    """Application secret key."""
    SECRET_KEY: str = Field(
        default_factory=lambda: binascii.hexlify(os.urandom(32)).decode(
            encoding="utf-8",
        ),
    )
    """Allowed CORS Origins"""
    ALLOWED_CORS_ORIGINS: list[str] | str = ["*"]
    """CSRF Cookie Name"""
    CSRF_COOKIE_NAME: str = "csrftoken"
    """CSRF Secure Cookie"""
    CSRF_COOKIE_SECURE: bool = False
    """JWT Encryption Algorithm"""
    JWT_ENCRYPTION_ALGORITHM: str = "HS256"
    """Default cache key expiration in seconds."""
    DEFAULT_CACHE_EXPIRATION: int = 60

    @property
    def FEATURES_PATH(self) -> str:
        """The path to JSON fixture files to load into tables."""
        return f"{BASE_DIR}/src/features"


class Settings(LiteStarSettings):
    """Settings for the project."""

    app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    log: LogSettings = Field(default_factory=LogSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
