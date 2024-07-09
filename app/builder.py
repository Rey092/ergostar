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
from litestar.template import TemplateConfig
from litestar.types import ControllerRouterHandler

from app.exception_handlers.base import exception_to_http_response
from config import settings
from src.infrastructure.plugins import plugins
from src.di.postgres import PostgresProvider
from src.presentation.api.health import HealthController
from src.di.landing import LandingProvider
from src.di.subscriptions import SubscriptionProvider


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
        extra_plugins: list = []

        # if settings.app.DEBUG:
        #     extra_plugins.append(plugins.admin)

        return extra_plugins

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
        exception_handlers.update(self.get_exception_handlers())

        app = Litestar(
            # cors_config=self.get_cors_config(),
            # # dependencies=dependencies,
            debug=settings.app.DEBUG,
            # openapi_config=self.get_openapi_config(),
            route_handlers=[HealthController, *self.get_route_handlers()],
            plugins=[
                plugins.app_config,
                plugins.structlog,
                plugins.alchemy,
                #     plugins.granian,
                *self.get_extra_plugins(),
            ],
            template_config=self.get_template_config(),
            # on_app_init=[auth.on_app_init],
            # listeners=[account_signals.user_created_event_handler,
            # team_signals.team_created_event_handler],
            exception_handlers=exception_handlers,
            compression_config=self.get_compression_config(),
        )

        # install dishka
        litestar_integration.setup_dishka(container, app)

        return app
