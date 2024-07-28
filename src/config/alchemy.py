"""Get the SQLAlchemy engine instance."""
from typing import Any
from advanced_alchemy.extensions.litestar import (
    AlembicAsyncConfig,
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    async_autocommit_before_send_handler,
)
from sqlalchemy import NullPool, event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from litestar.serialization import decode_json
from litestar.serialization import encode_json

from src.config.settings import DatabaseSettings


def get_alchemy_engine(db_settings: DatabaseSettings) -> AsyncEngine:
    """Get the SQLAlchemy engine instance."""

    # prepare the engine
    engine = create_async_engine(
        url=db_settings.url,
        future=True,
        json_serializer=encode_json,
        json_deserializer=decode_json,
        echo=db_settings.ECHO,
        echo_pool=db_settings.ECHO_POOL,
        max_overflow=db_settings.POOL_MAX_OVERFLOW,
        pool_size=db_settings.POOL_SIZE,
        pool_timeout=db_settings.POOL_TIMEOUT,
        pool_recycle=db_settings.POOL_RECYCLE,
        pool_pre_ping=db_settings.POOL_PRE_PING,
        pool_use_lifo=True,  # use lifo to reduce the number of idle connections
        poolclass=NullPool if db_settings.POOL_DISABLED else None,
    )

    # set up the JSONB column serialization
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

    return engine


def get_alchemy_config(engine: AsyncEngine, db_settings: DatabaseSettings) -> SQLAlchemyAsyncConfig:
    """Get SQLAlchemy configuration."""
    return SQLAlchemyAsyncConfig(
        engine_instance=engine,
        before_send_handler=async_autocommit_before_send_handler,
        session_config=AsyncSessionConfig(expire_on_commit=False),
        alembic_config=AlembicAsyncConfig(
            version_table_name=db_settings.migration_ddl_version_table,
            script_config=db_settings.migration_config,
            script_location=db_settings.migration_path,
        )
    )
