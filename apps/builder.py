"""Litestar application builder."""

from typing import Sequence

from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.static_files import StaticFilesConfig
from litestar.types import ControllerRouterHandler
from litestar.template import TemplateConfig

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
    def get_static_files_config() -> Sequence[StaticFilesConfig] | None:
        """Get a static files config."""
        return None

    @staticmethod
    def get_openapi_config() -> OpenAPIConfig | None:
        """Get OpenAPI config."""
        return None

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

        return Litestar(
            # cors_config=config.cors,
            # dependencies=dependencies,
            debug=settings.app.DEBUG,
            openapi_config=self.get_openapi_config(),
            route_handlers=self.get_route_handlers(),
            plugins=[
                # plugins.app_config,
                plugins.structlog,
                plugins.alchemy,
                #     plugins.vite,
                #     plugins.saq,
                #     plugins.granian,
            ],
            template_config=self.get_template_config(),
            static_files_config=self.get_static_files_config(),
            # on_app_init=[auth.on_app_init],
            # listeners=[account_signals.user_created_event_handler, team_signals.team_created_event_handler],
        )
