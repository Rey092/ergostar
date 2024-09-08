"""Base settings for the project."""

import binascii
import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

BASE_DIR: str = str(Path(__file__).parent.parent.parent.parent)


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
    """The name to use for the `alembic` versions table name."""
    MIGRATION_DDL_VERSION_TABLE: str = "ddl_version"

    @property
    def MIGRATION_PATH(self) -> str:
        """The path to the `alembic` database migrations."""
        return f"{BASE_DIR}/src/infrastructure/database/migrations"

    @property
    def MIGRATION_CONFIG(self) -> str:
        """The path to the `alembic.ini` configuration file."""
        return f"{self.MIGRATION_PATH}/alembic.ini"


class LogSettings(LiteStarSettings):
    """Logger configuration."""

    """Model configuration."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LOG_",
        extra="ignore",
        env_file_encoding="utf-8",
    )

    """Stdlib log levels. Only emit logs at this level, or higher."""
    LEVEL: int = 10
    """Level to log SQLAlchemy logs."""
    SQLALCHEMY_LEVEL: int = 20
    """Level to log uvicorn access logs."""
    UVICORN_ACCESS_LEVEL: int = 20
    """Level to log uvicorn error logs."""
    UVICORN_ERROR_LEVEL: int = 20

    """Telegram bot token."""
    TELEGRAM_BOT_TOKEN: str = ""
    """Telegram chat id."""
    TELEGRAM_CHAT_ID: str = ""
    """Enable Telegram logging."""
    TELEGRAM_LOGGING_ENABLED: bool = False


class RedisSettings(LiteStarSettings):
    """Redis settings."""

    """Model configuration."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="REDIS_",
        extra="ignore",
        env_file_encoding="utf-8",
    )

    """A Redis connection URL."""
    URL: str = "redis://localhost:6379/0"
    """Length of time to wait (in seconds) for a connection to become active."""
    SOCKET_CONNECT_TIMEOUT: int = 5
    """Length of time to wait (in seconds) before testing connection health."""
    HEALTH_CHECK_INTERVAL: int = 5
    """Length of time to wait (in seconds) between keepalive commands."""
    SOCKET_KEEPALIVE: bool = True


class AppSettings(LiteStarSettings):
    """Application configuration."""

    """Project name."""
    PROJECT_NAME: str = "Default"
    """Current container name."""
    CONTAINER_NAME: str = "Default"
    """The API base URL"""
    API_URL: str = "http://localhost:3000/docs"
    """Debug mode."""
    DEBUG: bool = True
    """Application secret key."""
    SECRET_KEY: str = Field(
        default_factory=lambda: binascii.hexlify(os.urandom(32)).decode(
            encoding="utf-8",
        ),
    )
    """API key hash digest size."""
    API_KEY_DIGEST_SIZE: int = 16
    """Allowed CORS Origins"""
    ALLOWED_CORS_ORIGINS: list[str] | str = ["*"]
    """CSRF Cookie Name"""
    CSRF_COOKIE_NAME: str = "csrftoken"
    """CSRF Secure Cookie"""
    CSRF_COOKIE_SECURE: bool = False
    """JWT Encryption Algorithm"""
    JWT_ENCRYPTION_ALGORITHM: str = "HS256"
    """Cache status."""
    CACHE_ENABLED: bool = True

    @property
    def FIXTURES_PATH(self) -> str:
        """The path to JSON fixture files to load into tables."""
        return f"{BASE_DIR}/src/infrastructure/disk/fixtures"


class VaultSettings(LiteStarSettings):
    """Secret vault settings."""

    """Model configuration."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="VAULT_",
        extra="ignore",
        env_file_encoding="utf-8",
    )

    """Vault URL."""
    URL: str = "http://localhost:8200"
    """Token to access vault."""
    TOKEN: str
    """Api Keys mount point path."""
    API_KEYS_MOUNT_POINT: str = "api-keys"


class Settings(LiteStarSettings):
    """Settings for the project."""

    app: AppSettings = Field(default_factory=AppSettings)
    vault: VaultSettings = Field(default_factory=VaultSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    log: LogSettings = Field(default_factory=LogSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
