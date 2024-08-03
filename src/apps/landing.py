"""Prepare ASGI application for landing."""

from pathlib import Path
from typing import TYPE_CHECKING

from advanced_alchemy.exceptions import RepositoryError
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.exceptions import HTTPException
from litestar.plugins.structlog import StructlogPlugin
from litestar.static_files import create_static_files_router
from litestar.template import TemplateConfig
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine

from src.apps.exception_handlers.base import exception_to_http_response
from src.apps.exception_handlers.dashboard import InternalServerExceptionHandler
from src.apps.exception_handlers.dashboard import not_found_exception_handler
from src.config.alchemy import get_alchemy_config
from src.config.alchemy import get_alchemy_engine
from src.config.ioc import BasicProvider
from src.config.litestar import get_compression_config
from src.config.litestar import get_cors_config
from src.config.litestar import get_structlog_config
from src.config.plugins import CachePlugin
from src.config.plugins import CLIPlugin
from src.config.redis import get_redis_engine
from src.config.settings import Settings
from src.features.core.ioc import CoreProvider
from src.features.core.routing import health_router
from src.features.landing.ioc import LandingProvider
from src.features.landing.routing import landing_router
from src.features.subscriptions.ioc import SubscriptionsProvider

if TYPE_CHECKING:
    from dishka import AsyncContainer


def create_app() -> Litestar:
    """Create application."""
    # create settings
    settings = Settings()

    # create sqlalchemy engine
    alchemy_engine: AsyncEngine = get_alchemy_engine(db_settings=settings.db)

    # create redis engine
    redis_engine: Redis = get_redis_engine(redis_settings=settings.redis)

    # create dependency container
    container: AsyncContainer = make_async_container(
        BasicProvider(),
        CoreProvider(),
        LandingProvider(),
        SubscriptionsProvider(),
        context={
            Settings: settings,
            AsyncEngine: alchemy_engine,
            Redis: redis_engine,
        },
    )

    # create app
    litestar_app = Litestar(
        cors_config=get_cors_config(app_settings=settings.app),
        debug=settings.app.DEBUG,
        route_handlers=[
            health_router,
            landing_router,
            create_static_files_router(
                path="/static",
                directories=["static/landing"],
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
                config=get_structlog_config(log_settings=settings.log),
            ),
            CachePlugin(redis=redis_engine, app_settings=settings.app),
            CLIPlugin(),
        ],
        template_config=TemplateConfig(
            directory=Path("templates"),
            engine=JinjaTemplateEngine,
        ),
        exception_handlers={
            RepositoryError: exception_to_http_response,
            HTTPException: not_found_exception_handler,
            Exception: InternalServerExceptionHandler(
                app_settings=settings.app,
            ),
        },
        compression_config=get_compression_config(),
    )

    # install dishka
    litestar_integration.setup_dishka(container, litestar_app)

    return litestar_app
