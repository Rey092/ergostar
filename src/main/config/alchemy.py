"""Get the SQLAlchemy configuration."""

from advanced_alchemy.extensions.litestar import AlembicAsyncConfig
from advanced_alchemy.extensions.litestar import AsyncSessionConfig
from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig
from advanced_alchemy.extensions.litestar import async_autocommit_before_send_handler
from sqlalchemy.ext.asyncio import AsyncEngine

from src.main.config.settings import DatabaseSettings


def get_alchemy_config(
    engine: AsyncEngine,
    db_settings: DatabaseSettings,
) -> SQLAlchemyAsyncConfig:
    """Get SQLAlchemy configuration."""
    return SQLAlchemyAsyncConfig(
        engine_instance=engine,
        before_send_handler=async_autocommit_before_send_handler,
        session_config=AsyncSessionConfig(expire_on_commit=False),
        alembic_config=AlembicAsyncConfig(
            version_table_name=db_settings.MIGRATION_DDL_VERSION_TABLE,
            script_config=db_settings.MIGRATION_CONFIG,
            script_location=db_settings.MIGRATION_PATH,
        ),
    )
