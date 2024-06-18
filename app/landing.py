"""Prepare ASGI application for landing."""

from collections.abc import Callable
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from litestar import Litestar
from litestar import Request
from litestar import Response
from litestar.config.cors import CORSConfig
from litestar.config.response_cache import ResponseCacheConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.exceptions import HTTPException
from litestar.static_files import create_static_files_router
from litestar.template import TemplateConfig
from litestar.types import ControllerRouterHandler

from app.builder import LitestarBuilder
from app.exception_handlers.landing import internal_server_exception_handler
from app.exception_handlers.landing import not_found_exception_handler
from config.plugins import cache_config
from config.plugins import cors
from src.landing.controller import LandingController


class LandingLitestarBuilder(LitestarBuilder):
    """Litestar application builder."""

    @staticmethod
    def response_cache_config() -> ResponseCacheConfig | None:
        """Get response cache config."""
        return cache_config

    @staticmethod
    def get_route_handlers() -> Sequence[ControllerRouterHandler] | None:
        """Get route handlers."""
        return [
            LandingController,
            create_static_files_router(
                path="/static",
                directories=["static/landing"],
                name="static",
            ),
            create_static_files_router(path="/media", directories=["."], name="media"),
        ]

    @staticmethod
    def get_cors_config() -> CORSConfig | None:
        """Get CORS config."""
        return cors

    @staticmethod
    def get_template_config() -> TemplateConfig | None:
        """Get template config."""
        return TemplateConfig(
            directory=Path("templates"),
            engine=JinjaTemplateEngine,
        )

    @staticmethod
    def get_exception_handlers() -> (
        dict[
            type[Exception],
            Callable[[Request[Any, Any, Any], Any], Response[Any]],
        ]
    ):
        """Get exception handlers."""
        return {
            HTTPException: not_found_exception_handler,
            Exception: internal_server_exception_handler,
        }


builder: LandingLitestarBuilder = LandingLitestarBuilder()
app: Litestar = builder.build()
