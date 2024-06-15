"""Base settings for the project."""

from typing import Any
from litestar.serialization import decode_json, encode_json
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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class DatabaseSettings(LiteStarSettings):
    """Database settings."""

    # Prepare database url Parts
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None

    @property
    def DATABASE_URL(self) -> str:
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

    # """Enable SQLAlchemy engine logs."""
    ECHO: bool = False
    # """Enable SQLAlchemy connection pool logs."""
    ECHO_POOL: bool = False
    # """Disable SQLAlchemy pool configuration."""
    POOL_DISABLED: bool = False
    # """Max overflow for SQLAlchemy connection pool"""
    POOL_MAX_OVERFLOW: int = False
    # """Pool size for SQLAlchemy connection pool"""
    POOL_SIZE: int = 5
    # """Time in seconds for timing connections out of the connection pool."""
    POOL_TIMEOUT: int = 30
    # """Amount of time to wait before recycling connections."""
    POOL_RECYCLE: int = 300
    """Optionally ping database before fetching a session from the connection pool."""
    POOL_PRE_PING: bool = False
    # """The path to the `alembic.ini` configuration file."""
    # MIGRATION_CONFIG: str = f"{BASE_DIR}/db/migrations/alembic.ini"
    # """The path to the `alembic` database migrations."""
    # MIGRATION_PATH: str = f"{BASE_DIR}/db/migrations"
    # """The name to use for the `alembic` versions table name."""
    # MIGRATION_DDL_VERSION_TABLE: str = "ddl_version"
    # """The path to JSON fixture files to load into tables."""
    # FIXTURE_PATH: str = f"{BASE_DIR}/db/fixtures"

    """SQLAlchemy engine instance generated from settings."""
    _engine_instance: AsyncEngine | None = None

    @property
    def engine(self) -> AsyncEngine:
        return self.get_engine()

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance is not None:
            return self._engine_instance
        if self.DATABASE_URL.startswith("postgresql+asyncpg"):
            engine = create_async_engine(
                url=self.DATABASE_URL,
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
        elif self.DATABASE_URL.startswith("sqlite+aiosqlite"):
            engine = create_async_engine(
                url=self.DATABASE_URL,
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
                url=self.DATABASE_URL,
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


class Settings(LiteStarSettings):
    """Settings for the project."""

    # app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    # vite: ViteSettings = Field(default_factory=ViteSettings)
    # server: ServerSettings = Field(default_factory=ServerSettings)
    # log: LogSettings = Field(default_factory=LogSettings)
    # redis: RedisSettings = Field(default_factory=RedisSettings)
    # saq: SaqSettings = Field(default_factory=SaqSettings)
