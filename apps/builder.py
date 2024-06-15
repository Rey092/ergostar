"""Litestar application builder."""

from litestar import Litestar


class LitestarBuilder:
    """Litestar application builder."""

    @staticmethod
    def build(**kwargs) -> Litestar:
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
        # settings = get_settings()

        return Litestar(
            # cors_config=config.cors,
            # dependencies=dependencies,
            # debug=settings.app.DEBUG,
            # openapi_config=openapi.config,
            # route_handlers=routers.route_handlers,
            # plugins=[
            #     plugins.app_config,
            #     plugins.structlog,
            #     plugins.alchemy,
            #     plugins.vite,
            #     plugins.saq,
            #     plugins.granian,
            # ],
            # on_app_init=[auth.on_app_init],
            # listeners=[account_signals.user_created_event_handler, team_signals.team_created_event_handler],
            **kwargs
        )
