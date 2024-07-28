"""Litestar application builder."""

from collections.abc import Callable
from collections.abc import Sequence
from typing import Any

from advanced_alchemy.exceptions import RepositoryError
from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar import Request
from litestar import Response
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.template import TemplateConfig
from litestar.types import ControllerRouterHandler

from src.apps.exception_handlers.base import exception_to_http_response
from src.config import settings
from src.config.plugins import plugins
from src.config.di import PostgresProvider
from src.config.di import LandingProvider
from src.config.di import SubscriptionProvider
from src.config.plugins.plugins import get_alchemy, get_app_config
from src.core.routing import health_router


class LitestarBuilder:
    """Litestar application builder."""

    @staticmethod
    def get_route_handlers() -> Sequence[ControllerRouterHandler]:
        """Get route handlers."""
        return []

    @staticmethod
    def get_template_config() -> TemplateConfig | None:
        """Get template config."""
        return None

    @staticmethod
    def get_openapi_config() -> OpenAPIConfig | None:
        """Get OpenAPI config."""
        return None

    @staticmethod
    def get_extra_plugins() -> Sequence:
        """Get extra plugins."""
        return []

    @staticmethod
    def get_cors_config() -> CORSConfig | None:
        """Get CORS config."""
        return None

    @staticmethod
    def get_exception_handlers() -> (
        dict[
            type[Exception],
            Callable[[Request[Any, Any, Any], Any], Response[Any]],
        ]
    ):
        """Get exception handlers."""
        return {}

    @staticmethod
    def get_compression_config() -> Any | None:
        """Get compression config."""
        return None

    def build(self) -> Litestar:
        """Create ASGI application."""
        from litestar import Litestar

        container = make_async_container(
            PostgresProvider(),
            LandingProvider(),
            SubscriptionProvider(),
        )

        # prepare exception handlers
        exception_handlers: dict = {
            RepositoryError: exception_to_http_response,
        }
        if not settings.app.DEBUG:
            exception_handlers.update(self.get_exception_handlers())

        app = Litestar(
            cors_config=self.get_cors_config(),
            # # dependencies=dependencies,
            debug=settings.app.DEBUG,
            # openapi_config=self.get_openapi_config(),
            route_handlers=[health_router, *self.get_route_handlers()],
            plugins=[
                get_app_config(),
                plugins.structlog,
                get_alchemy(),
                *self.get_extra_plugins(),
            ],
            template_config=self.get_template_config(),
            # on_app_init=[auth.on_app_init],
            # listeners=[account_signals.user_created_event_handler,
            # team_signals.team_created_event_handler],
            exception_handlers=exception_handlers,
            compression_config=self.get_compression_config(),
            openapi_config=OpenAPIConfig(
                title="Litestar",
                version="0.1.0",
                description="Litestar API",
                path="/docs",
                render_plugins=[
                    SwaggerRenderPlugin()
                ]
            )
        )

        # install dishka
        litestar_integration.setup_dishka(container, app)

        return app
