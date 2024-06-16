"""Litestar application builder."""

from collections.abc import Callable
from collections.abc import Sequence
from typing import Any

from advanced_alchemy.exceptions import RepositoryError
from litestar import Litestar
from litestar import Request
from litestar import Response
from litestar.config.cors import CORSConfig
from litestar.config.response_cache import ResponseCacheConfig
from litestar.openapi import OpenAPIConfig
from litestar.stores.base import Store
from litestar.stores.registry import StoreRegistry
from litestar.template import TemplateConfig
from litestar.types import ControllerRouterHandler

from app.exception_handlers.base import exception_to_http_response
from config import settings
from server import plugins


class LitestarBuilder:
    """Litestar application builder."""

    @staticmethod
    def get_route_handlers() -> Sequence[ControllerRouterHandler] | None:
        """Get route handlers."""
        return None

    @staticmethod
    def get_template_config() -> TemplateConfig | None:
        """Get template config."""
        return None

    @staticmethod
    def get_openapi_config() -> OpenAPIConfig | None:
        """Get OpenAPI config."""
        return None

    @staticmethod
    def get_stores() -> StoreRegistry | dict[str, Store] | None:
        """Get stores."""
        return None

    @staticmethod
    def response_cache_config() -> ResponseCacheConfig | None:
        """Get response cache config."""
        return None

    @staticmethod
    def get_extra_plugins() -> Sequence:
        """Get extra plugins."""
        extra_plugins: list = []

        if settings.app.DEBUG:
            extra_plugins.append(plugins.admin)

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

    def build(self) -> Litestar:
        """Create ASGI application."""
        from litestar import Litestar

        # from app.config import app as config
        # from app.config import constants
        # from app.config.base import get_settings
        # from app.domain.accounts import signals as account_signals
        # from app.domain.accounts.dependencies import provide_user
        # from app.domain.accounts.guards import auth
        # from app.domain.teams import signals as team_signals
        # from app.lib.dependencies import create_collection_dependencies
        # from app.server import openapi, plugins, routers

        # dependencies = {constants.USER_DEPENDENCY_KEY: Provide(provide_user)}
        # dependencies.update(create_collection_dependencies())

        # prepare exception handlers
        exception_handlers: dict = {
            RepositoryError: exception_to_http_response,
        }
        exception_handlers.update(self.get_exception_handlers())

        return Litestar(
            # cors_config=config.cors,
            # dependencies=dependencies,
            debug=settings.app.DEBUG,
            openapi_config=self.get_openapi_config(),
            route_handlers=self.get_route_handlers(),
            plugins=[
                plugins.app_config,
                # plugins.structlog,
                plugins.alchemy,
                #     plugins.vite,
                #     plugins.saq,
                #     plugins.granian,
                # *self.get_extra_plugins(),
            ],
            template_config=self.get_template_config(),
            # on_app_init=[auth.on_app_init],
            # listeners=[account_signals.user_created_event_handler,
            # team_signals.team_created_event_handler],
            stores=self.get_stores(),
            response_cache_config=self.response_cache_config(),
            exception_handlers=exception_handlers,
            cors_config=self.get_cors_config(),
        )
