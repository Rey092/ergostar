"""Basic provider (DI)."""

from collections.abc import AsyncIterable

from dishka import AnyOf
from dishka import Scope
from dishka import from_context
from dishka import provide
from dishka.provider import Provider
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.common.interfaces.database_session import IAlchemySession
from src.common.interfaces.database_session import IDatabaseSession
from src.config.settings import AppSettings
from src.config.settings import Settings
from src.config.settings import VaultSettings


class BasicProvider(Provider):
    """Basic provider (DI)."""

    settings = from_context(provides=Settings, scope=Scope.APP)
    async_engine = from_context(provides=AsyncEngine, scope=Scope.APP)
    redis_engine = from_context(provides=Redis, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_app_settings(self, all_settings: Settings) -> AppSettings:
        """Provide debug app status."""
        return all_settings.app

    @provide(scope=Scope.APP)
    def get_vault_settings(self, all_settings: Settings) -> VaultSettings:
        """Provide debug app status."""
        return all_settings.vault

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

    @provide(scope=Scope.REQUEST, provides=AnyOf[IAlchemySession, IDatabaseSession])
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[IAlchemySession]:
        """Provide async session."""
        async with session_maker() as session:
            yield session
