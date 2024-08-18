"""Prepare ASGI application for landing."""

from typing import TYPE_CHECKING

from advanced_alchemy.exceptions import RepositoryError
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from cashews import cache
from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from hvac import Client as VaultEngine
from hvac.exceptions import VaultError
from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.plugins.structlog import StructlogPlugin
from litestar.static_files import create_static_files_router
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.status_codes import HTTP_503_SERVICE_UNAVAILABLE
from redis.asyncio import Redis as RedisEngine
from sqlalchemy.ext.asyncio import AsyncEngine

from src.apps.exception_handlers.repository_alchemy import (
    repository_alchemy_exception_handler,
)
from src.apps.exception_handlers.repository_vault import (
    repository_vault_exception_handler,
)
from src.apps.exception_handlers.server import server_exception_handler
from src.config.alchemy import get_alchemy_config
from src.config.alchemy import get_alchemy_engine
from src.config.cli import CLIPlugin
from src.config.ioc import BasicProvider
from src.config.litestar import get_cors_config
from src.config.litestar import get_structlog_config
from src.config.redis import get_redis_engine
from src.config.settings import Settings
from src.config.vault import get_vault_engine
from src.features.auth.ioc import AuthProvider
from src.features.auth.routing import auth_router
from src.features.auth.security.api_key.auth import api_key_auth
from src.features.core.ioc import CoreProvider
from src.features.core.routing import health_router
from src.features.subscriptions.ioc import SubscriptionsProvider
from src.features.users.ioc import UserProvider

if TYPE_CHECKING:
    from dishka import AsyncContainer


def create_app() -> Litestar:
    """Create application."""
    # create settings
    settings = Settings()

    # create sqlalchemy engine
    alchemy_engine: AsyncEngine = get_alchemy_engine(db_settings=settings.db)

    # create redis engine
    redis_engine: RedisEngine = get_redis_engine(redis_settings=settings.redis)

    # create vault engine
    vault_engine: VaultEngine = get_vault_engine(vault_settings=settings.vault)

    # initialize cache
    cache.setup(
        settings_url=settings.redis.URL,
        disable=settings.app.CACHE_ENABLED,
    )

    # create dependency container
    container: AsyncContainer = make_async_container(
        CoreProvider(),
        BasicProvider(),
        SubscriptionsProvider(),
        UserProvider(),
        AuthProvider(),
        context={
            Settings: settings,
            AsyncEngine: alchemy_engine,
            RedisEngine: redis_engine,
            VaultEngine: vault_engine,
        },
    )

    # create app
    litestar_app = Litestar(
        cors_config=get_cors_config(app_settings=settings.app),
        debug=settings.app.DEBUG,
        route_handlers=[
            health_router,
            auth_router,
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
        exception_handlers={
            RepositoryError: repository_alchemy_exception_handler,
            VaultError: repository_vault_exception_handler,
            HTTP_500_INTERNAL_SERVER_ERROR: server_exception_handler,
            HTTP_503_SERVICE_UNAVAILABLE: server_exception_handler,
        },
        on_app_init=[
            api_key_auth.on_app_init,
        ],
        openapi_config=OpenAPIConfig(
            title="Litestar API",
            version="0.1.0",
            description="Litestar API",
            use_handler_docstrings=True,
            path="/docs",
            render_plugins=[
                SwaggerRenderPlugin(),
            ],
        ),
    )

    # install dishka
    litestar_integration.setup_dishka(container, litestar_app)

    return litestar_app
