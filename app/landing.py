"""Prepare ASGI application for landing."""

from pathlib import Path
from typing import Sequence

from litestar import Litestar
from litestar.config.response_cache import ResponseCacheConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import StaticFilesConfig
from litestar.stores.base import Store
from litestar.stores.registry import StoreRegistry
from litestar.template import TemplateConfig
from litestar.types import ControllerRouterHandler

from app.builder import LitestarBuilder
from config.plugins import redis_store, cache_config
from src.landing.controller import LandingController


class LandingLitestarBuilder(LitestarBuilder):
    """Litestar application builder."""

    @staticmethod
    def get_stores() -> StoreRegistry | dict[str, Store] | None:
        """Get stores."""
        return {"redis_backed_store": redis_store}

    @staticmethod
    def response_cache_config() -> ResponseCacheConfig | None:
        """Get response cache config."""
        return cache_config

    @staticmethod
    def get_route_handlers() -> Sequence[ControllerRouterHandler] | None:
        """Get route handlers."""
        return [LandingController]

    @staticmethod
    def get_template_config() -> TemplateConfig | None:
        """Get template config."""
        return TemplateConfig(
            directory=Path("templates"),
            engine=JinjaTemplateEngine,
        )

    @staticmethod
    def get_static_files_config() -> Sequence[StaticFilesConfig] | None:
        """Get a static files config."""
        return (
            StaticFilesConfig(
                directories=["static/landing/css"],
                path="/static/landing/css",
                name="css",
            ),
            StaticFilesConfig(
                directories=["static/landing/js"], path="/static/landing/js", name="js"
            ),
            StaticFilesConfig(
                directories=["static/landing/img"],
                path="/static/landing/img",
                name="img",
            ),
        )


builder: LandingLitestarBuilder = LandingLitestarBuilder()
app: Litestar = builder.build()
