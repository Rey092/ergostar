"""Base settings for the project."""

import binascii
import json
import os
from pathlib import Path
from typing import Any

from advanced_alchemy.utils.text import slugify
from litestar.data_extractors import RequestExtractorField
from litestar.data_extractors import ResponseExtractorField
from litestar.serialization import decode_json
from litestar.serialization import encode_json
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from redis.asyncio import Redis
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool


class LiteStarSettings(BaseSettings):
    """Abstract settings."""

    # prepare model config
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # prepare base directory
    BASE_DIR: str = str(Path(__file__).parent.parent.parent)


class UnfoldSettings(LiteStarSettings):
    """Unfold Admin Panel settings."""

    # prepare model config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="UNFOLD_"
    )

    # Debug mode.
    DEBUG: bool = True

    # Key to use for signing cookies.
    SECRET_KEY: str = Field(
        default_factory=lambda: binascii.hexlify(os.urandom(32)).decode(
            encoding="utf-8"
        )
    )

    # The allowed hosts for the Django admin panel.
    ALLOWED_HOSTS: list[str] = ["*"]


class DatabaseSettings(LiteStarSettings):
    """Database settings."""

    # prepare model config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="POSTGRES_"
    )

    """Database URL parts."""
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str | None = None
    PASSWORD: str | None = None
    DB: str | None = None

    @property
    def url(self) -> str:
        """Database URL."""
        if all([self.USER, self.PASSWORD, self.DB]):
            url = (
                f"postgresql+asyncpg://"
                f"{self.USER}:"
                f"{self.PASSWORD}@"
                f"{self.HOST}:"
                f"{self.PORT}/"
                f"{self.DB}"
            )
        else:
            url = "sqlite+aiosqlite:///db.sqlite3"
        return str(url)

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
        return f"{self.BASE_DIR}/src/infra/postgres/migrations/alembic.ini"

    @property
    def migration_path(self) -> str:
        """The path to the `alembic` database migrations."""
        return f"{self.BASE_DIR}/src/infra/postgres/migrations"

    @property
    def fixture_path(self) -> str:
        """The path to JSON fixture files to load into tables."""
        return f"{self.BASE_DIR}/src/infra/postgres/fixtures"

    """SQLAlchemy engine instance generated from settings."""
    _engine_instance: AsyncEngine | None = None

    @property
    def engine(self) -> AsyncEngine:
        return self.get_engine()

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance is not None:
            return self._engine_instance
        if self.url.startswith("postgresql+asyncpg"):
            engine = create_async_engine(
                url=self.url,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
                pool_use_lifo=True,  # use lifo to reduce the number of idle connections
                poolclass=NullPool if self.POOL_DISABLED else None,
            )
            """Database session factory.

            See [`async_sessionmaker()`][sqlalchemy.ext.asyncio.async_sessionmaker].
            """

            @event.listens_for(engine.sync_engine, "connect")
            def _sqla_on_connect(
                dbapi_connection: Any, _: Any
            ) -> Any:  # pragma: no cover
                """Using msgspec for serialization of the json column values means that the
                output is binary, not `str` like `json.dumps` would output.
                SQLAlchemy expects that the json serializer returns `str` and calls `.encode()` on the value to
                turn it to bytes before writing to the JSONB column. I'd need to either wrap `serialization.to_json` to
                return a `str` so that SQLAlchemy could then convert it to binary, or do the following, which
                changes the behaviour of the dialect to expect a binary value from the serializer.
                See Also https://github.com/sqlalchemy/sqlalchemy/blob/14bfbadfdf9260a1c40f63b31641b27fe9de12a0/lib/sqlalchemy/dialects/postgresql/asyncpg.py#L934  pylint: disable=line-too-long
                """

                def encoder(bin_value: bytes) -> bytes:
                    return b"\x01" + encode_json(bin_value)

                def decoder(bin_value: bytes) -> Any:
                    # the byte is the \x01 prefix for jsonb used by PostgreSQL.
                    # asyncpg returns it when format='binary'
                    return decode_json(bin_value[1:])

                dbapi_connection.await_(
                    dbapi_connection.driver_connection.set_type_codec(
                        "jsonb",
                        encoder=encoder,
                        decoder=decoder,
                        schema="pg_catalog",
                        format="binary",
                    ),
                )
                dbapi_connection.await_(
                    dbapi_connection.driver_connection.set_type_codec(
                        "json",
                        encoder=encoder,
                        decoder=decoder,
                        schema="pg_catalog",
                        format="binary",
                    ),
                )
        elif self.url.startswith("sqlite+aiosqlite"):
            engine = create_async_engine(
                url=self.url,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
            )
            """Database session factory.

            See [`async_sessionmaker()`][sqlalchemy.ext.asyncio.async_sessionmaker].
            """

            @event.listens_for(engine.sync_engine, "connect")
            def _sqla_on_connect(
                dbapi_connection: Any, _: Any
            ) -> Any:  # pragma: no cover
                """Override the default begin statement.

                The disables the built-in begin execution.
                """
                dbapi_connection.isolation_level = None

            @event.listens_for(engine.sync_engine, "begin")
            def _sqla_on_begin(dbapi_connection: Any) -> Any:  # pragma: no cover
                """Emits a custom begin"""
                dbapi_connection.exec_driver_sql("BEGIN")
        else:
            engine = create_async_engine(
                url=self.url,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
            )
        self._engine_instance = engine
        return self._engine_instance


class LogSettings(LiteStarSettings):
    """Logger configuration"""

    # https://stackoverflow.com/a/1845097/6560549
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
    """
    Attributes of the SAQ.

    [`Job`](https://github.com/tobymao/saq/blob/master/saq/job.py) to be
    logged.
    """
    JOB_FIELDS: list[str] = [
        "function",
        "kwargs",
        "key",
        "scheduled",
        "attempts",
        "completed",
        "queued",
        "started",
        "result",
        "error",
    ]
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
    """Level to log SAQ logs."""
    SAQ_LEVEL: int = 20
    """Level to log SQLAlchemy logs."""
    SQLALCHEMY_LEVEL: int = 20
    """Level to log uvicorn access logs."""
    UVICORN_ACCESS_LEVEL: int = 20
    """Level to log uvicorn error logs."""
    UVICORN_ERROR_LEVEL: int = 20
    """Level to log uvicorn access logs."""
    GRANIAN_ACCESS_LEVEL: int = 30
    """Level to log uvicorn error logs."""
    GRANIAN_ERROR_LEVEL: int = 20


class RedisSettings(LiteStarSettings):
    """Redis settings."""

    # A Redis connection URL.
    URL: str = "redis://localhost:6379/0"
    # Length of time to wait (in seconds) for a connection to become active
    SOCKET_CONNECT_TIMEOUT: int = 5
    # Length of time to wait (in seconds) before testing connection health
    HEALTH_CHECK_INTERVAL: int = 5
    # Length of time to wait (in seconds) between keepalive commands
    SOCKET_KEEPALIVE: bool = True
    # Redis instance generated from settings
    _redis_instance: Redis | None = None

    @property
    def client(self) -> Redis:
        return self.get_client()

    def get_client(self) -> Redis:
        if self._redis_instance is not None:
            return self._redis_instance
        self._redis_instance = Redis.from_url(
            url=self.URL,
            encoding="utf-8",
            decode_responses=False,
            socket_connect_timeout=self.SOCKET_CONNECT_TIMEOUT,
            socket_keepalive=self.SOCKET_KEEPALIVE,
            health_check_interval=self.HEALTH_CHECK_INTERVAL,
        )
        return self._redis_instance


class AppSettings(LiteStarSettings):
    """Application configuration"""

    """The frontend base URL"""
    URL: str = "http://localhost:8000"
    """Run `Litestar` with `debug=True`."""
    DEBUG: bool = True
    """Application secret key."""
    SECRET_KEY: str = Field(
        default_factory=lambda: binascii.hexlify(os.urandom(32)).decode(
            encoding="utf-8"
        )
    )
    """Application name."""
    NAME: str = "app"
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
    def slug(self) -> str:
        """Return a slugified name.

        Returns
        -------
            `self.NAME`, all lowercase and hyphens instead of spaces.

        """
        return slugify(self.NAME)


class Settings(LiteStarSettings):
    """Settings for the project."""

    app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    unfold: UnfoldSettings = Field(default_factory=UnfoldSettings)
    log: LogSettings = Field(default_factory=LogSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    # server: ServerSettings = Field(default_factory=ServerSettings)
    # saq: SaqSettings = Field(default_factory=SaqSettings)
