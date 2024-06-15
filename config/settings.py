"""Base settings for the project."""

import binascii
import json
import os
from typing import Any

from advanced_alchemy.utils.text import slugify
from litestar.data_extractors import RequestExtractorField, ResponseExtractorField
from litestar.serialization import decode_json, encode_json
from redis.asyncio import Redis
from sqlalchemy import event, URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool
from pydantic import (
    Field,
    PostgresDsn,
)

from pydantic_settings import BaseSettings, SettingsConfigDict


class LiteStarSettings(BaseSettings):
    """Abstract settings."""

    # prepare model config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # prepare base directory
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DatabaseSettings(LiteStarSettings):
    """Database settings."""

    """Database URL parts."""
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None

    @property
    def URL(self) -> str:
        """Database URL."""
        if all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB]):
            url: PostgresDsn = URL.create(
                drivername="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                database=self.POSTGRES_DB,
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
    POOL_MAX_OVERFLOW: int = False
    """Pool size for SQLAlchemy connection pool"""
    POOL_SIZE: int = 5
    """Time in seconds for timing connections out of the connection pool."""
    POOL_TIMEOUT: int = 30
    """Amount of time to wait before recycling connections."""
    POOL_RECYCLE: int = 300
    """Optionally ping database before fetching a session from the connection pool."""
    POOL_PRE_PING: bool = False

    @property
    def MIGRATION_CONFIG(self) -> str:
        """The path to the `alembic.ini` configuration file."""
        return f"{self.BASE_DIR}/src/db/migrations/alembic.ini"

    @property
    def MIGRATION_PATH(self) -> str:
        """The path to the `alembic` database migrations."""
        return f"{self.BASE_DIR}/src/db/migrations"

    @property
    def MIGRATION_DDL_VERSION_TABLE(self) -> str:
        """The name to use for the `alembic` versions table name."""
        return "ddl_version"

    @property
    def FIXTURE_PATH(self) -> str:
        """The path to JSON fixture files to load into tables."""
        return f"{self.BASE_DIR}/db/fixtures"

    """SQLAlchemy engine instance generated from settings."""
    _engine_instance: AsyncEngine | None = None

    @property
    def engine(self) -> AsyncEngine:
        return self.get_engine()

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance is not None:
            return self._engine_instance
        if self.URL.startswith("postgresql+asyncpg"):
            engine = create_async_engine(
                url=self.URL,
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
        elif self.URL.startswith("sqlite+aiosqlite"):
            engine = create_async_engine(
                url=self.URL,
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
                """
                Override the default begin statement.

                The disables the built-in begin execution.
                """
                dbapi_connection.isolation_level = None

            @event.listens_for(engine.sync_engine, "begin")
            def _sqla_on_begin(dbapi_connection: Any) -> Any:  # pragma: no cover
                """Emits a custom begin"""
                dbapi_connection.exec_driver_sql("BEGIN")
        else:
            engine = create_async_engine(
                url=self.URL,
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

    @property
    def slug(self) -> str:
        """Return a slugified name.

        Returns:
            `self.NAME`, all lowercase and hyphens instead of spaces.
        """
        return slugify(self.NAME)

    def __post_init__(self) -> None:
        # Check if the ALLOWED_CORS_ORIGINS is a string.
        if isinstance(self.ALLOWED_CORS_ORIGINS, str):
            # Check if the string starts with "[" and ends with "]", indicating a list.
            if self.ALLOWED_CORS_ORIGINS.startswith(
                "["
            ) and self.ALLOWED_CORS_ORIGINS.endswith("]"):
                try:
                    # Safely evaluate the string as a Python list.
                    self.ALLOWED_CORS_ORIGINS = json.loads(self.ALLOWED_CORS_ORIGINS)
                except (SyntaxError, ValueError):
                    # Handle potential errors if the string is not a valid Python literal.
                    msg = "ALLOWED_CORS_ORIGINS is not a valid list representation."
                    raise ValueError(msg) from None
            else:
                # Split the string by commas into a list if it is not meant to be a list representation.
                self.ALLOWED_CORS_ORIGINS = [
                    host.strip() for host in self.ALLOWED_CORS_ORIGINS.split(",")
                ]


class Settings(LiteStarSettings):
    """Settings for the project."""

    app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    # vite: ViteSettings = Field(default_factory=ViteSettings)
    # server: ServerSettings = Field(default_factory=ServerSettings)
    log: LogSettings = Field(default_factory=LogSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    # saq: SaqSettings = Field(default_factory=SaqSettings)
