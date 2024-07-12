"""Application configuration plugin."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING
from typing import TypeVar

from litestar.config.response_cache import ResponseCacheConfig
from litestar.config.response_cache import default_cache_key_builder
from litestar.plugins import CLIPluginProtocol
from litestar.plugins import InitPluginProtocol
from litestar.stores.redis import RedisStore
from litestar.stores.registry import StoreRegistry

from src.infra import settings

if TYPE_CHECKING:
    from click import Group
    from litestar import Request
    from litestar.config.app import AppConfig
    from redis.asyncio import Redis


T = TypeVar("T")


class ApplicationConfigurator(InitPluginProtocol, CLIPluginProtocol):
    """Application configuration plugin."""

    __slots__ = ("redis", "app_slug")
    redis: Redis
    app_slug: str

    # noinspection PyTypeChecker
    def on_cli_init(self, cli: Group) -> None:
        """Add commands to the CLI."""
        from src.presentation.cli import init_group
        from src.presentation.cli import users_group

        self.redis = settings.redis.get_client()
        self.app_slug = settings.app.slug

        cli.add_command(init_group)
        cli.add_command(users_group)

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """
        Configure application for use with SQLAlchemy.

        Args:
        ----
            app_config: The :class:`AppConfig <.config.app.AppConfig>` instance.
        """
        from src.infra import settings
        # import models module to initialize the imperative mapping
        from src.infra.postgres import models  # noqa

        self.redis = settings.redis.get_client()
        self.app_slug = settings.app.slug
        app_config.response_cache_config = ResponseCacheConfig(
            default_expiration=settings.app.DEFAULT_CACHE_EXPIRATION,
            key_builder=self._cache_key_builder,
        )
        app_config.stores = StoreRegistry(default_factory=self.redis_store_factory)
        app_config.on_shutdown.append(self.redis.aclose)  # type: ignore[attr-defined]
        return app_config

    def redis_store_factory(self, name: str) -> RedisStore:
        """Create a Redis store for the application."""
        return RedisStore(self.redis, namespace=f"{self.app_slug}:{name}")

    def _cache_key_builder(self, request: Request) -> str:
        """App name prefixed cache key builder.

        For development, a random UUID is used as the cache key to prevent
        caching. For production, the app slug is prefixed to the default cache

        Args:
        ----
            request (Request): Current request instance.

        Returns:
        -------
            str: App slug prefixed cache key.

        """
        if settings.app.DEBUG:
            return str(uuid.uuid4())

        return f"{self.app_slug}:{default_cache_key_builder(request)}"
