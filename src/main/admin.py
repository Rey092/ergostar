"""Prepare ASGI application for landing.

TODO: App in development
"""

from pathlib import Path
from typing import TYPE_CHECKING

from advanced_alchemy.exceptions import RepositoryError
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from cashews import cache
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.plugins.structlog import StructlogPlugin
from litestar.static_files import create_static_files_router
from litestar.template import TemplateConfig

from src.infrastructure.database.engine import get_alchemy_engine
from src.infrastructure.redis.engine import get_redis_engine
from src.infrastructure.vault.engine import get_vault_engine
from src.main.config.alchemy import get_alchemy_config
from src.main.config.cli import CLIPlugin
from src.main.config.compression import get_compression_config
from src.main.config.container import get_async_container
from src.main.config.cors import get_cors_config
from src.main.config.logging import get_structlog_config
from src.main.config.settings import Settings
from src.main.exception_handlers.repository_alchemy import (
    repository_alchemy_exception_handler,
)
from src.presentation.routing import admin_router

if TYPE_CHECKING:
    from dishka import AsyncContainer
    from hvac import Client as VaultEngine
    from redis.asyncio import Redis
    from sqlalchemy.ext.asyncio import AsyncEngine


def create_app() -> Litestar:
    """Create application."""
    # create settings
    settings = Settings()

    # create sqlalchemy engine
    alchemy_engine: AsyncEngine = get_alchemy_engine(db_settings=settings.db)

    # create redis engine
    redis_engine: Redis = get_redis_engine(redis_settings=settings.redis)

    # create vault engine
    vault_engine: VaultEngine = get_vault_engine(vault_settings=settings.vault)

    # create dependency container
    container: AsyncContainer = get_async_container(
        settings=settings,
        alchemy_engine=alchemy_engine,
        redis_engine=redis_engine,
        vault_engine=vault_engine,
    )

    # initialize cache
    cache.setup(
        settings_url=settings.redis.URL,
        disable=settings.app.CACHE_ENABLED,
    )

    # create app
    litestar_app = Litestar(
        cors_config=get_cors_config(app_settings=settings.app),
        debug=settings.app.DEBUG,
        route_handlers=[
            admin_router,
            create_static_files_router(
                path="/static",
                directories=["static/admin"],
                name="static",
            ),
            create_static_files_router(
                path="/media",
                directories=["."],
                name="media",
            ),
        ],
        plugins=[
            SQLAlchemyPlugin(
                config=get_alchemy_config(
                    engine=alchemy_engine,
                    db_settings=settings.db,
                ),
            ),
            StructlogPlugin(
                config=get_structlog_config(
                    app_settings=settings.app,
                    log_settings=settings.log,
                ),
            ),
            CLIPlugin(),
        ],
        template_config=TemplateConfig(
            directory=Path("templates"),
            engine=JinjaTemplateEngine,
        ),
        exception_handlers={
            RepositoryError: repository_alchemy_exception_handler,
        },
        compression_config=get_compression_config(),
    )

    # install dishka
    litestar_integration.setup_dishka(container, litestar_app)

    return litestar_app
