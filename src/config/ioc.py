"""Basic provider (DI)."""

from collections.abc import AsyncIterable
from dishka import Scope, from_context
from dishka import provide
from dishka.provider import Provider
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.common.interfaces.db import IDatabaseSession
from src.common.types import SETTINGS_DEBUG, SETTINGS_FEATURES_PATH
from src.config.settings import Settings


class BasicProvider(Provider):
    """Basic provider (DI)."""

    settings = from_context(provides=Settings, scope=Scope.APP)
    async_engine = from_context(provides=AsyncEngine, scope=Scope.APP)
    redis_engine = from_context(provides=Redis, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_debug(self, all_settings: Settings) -> SETTINGS_DEBUG:
        """Provide debug app status."""
        return all_settings.app.DEBUG

    @provide(scope=Scope.APP)
    def get_features_path(self, all_settings: Settings) -> SETTINGS_FEATURES_PATH:
        """Provide a features' path."""
        return all_settings.app.FEATURES_PATH

    @provide(scope=Scope.APP)
    def get_session_maker(
        self,
        async_engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        """Provide async session maker."""
        return async_sessionmaker(
            async_engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[IDatabaseSession]:
        """Provide async session."""
        async with session_maker() as session:
            async with session.begin():
                yield session
