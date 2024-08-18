"""Basic provider (DI)."""

from collections.abc import AsyncIterable

from dishka import AnyOf
from dishka import Scope
from dishka import from_context
from dishka import provide
from dishka.provider import Provider
from hvac import Client as VaultEngine
from redis.asyncio import Redis as RedisEngine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.common.base.vault_uow import VaultSession
from src.common.interfaces.unit_of_work import IDatabaseSession
from src.common.interfaces.unit_of_work import IVaultSession
from src.config.settings import AppSettings
from src.config.settings import Settings
from src.config.settings import VaultSettings


class BasicProvider(Provider):
    """Basic provider (DI)."""

    settings = from_context(provides=Settings, scope=Scope.APP)
    async_engine = from_context(provides=AsyncEngine, scope=Scope.APP)
    redis_engine = from_context(provides=RedisEngine, scope=Scope.APP)
    vault_engine = from_context(provides=VaultEngine, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_app_settings(self, all_settings: Settings) -> AppSettings:
        """Provide debug app status."""
        return all_settings.app

    @provide(scope=Scope.APP)
    def get_vault_settings(self, all_settings: Settings) -> VaultSettings:
        """Provide debug app status."""
        return all_settings.vault

    @provide(scope=Scope.APP)
    def get_alchemy_session_maker(
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
    async def get_alchemy_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, IDatabaseSession]]:
        """Provide async session."""
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_vault_session(
        self,
        vault_engine: VaultEngine,
    ) -> AsyncIterable[AnyOf[VaultSession, IVaultSession]]:
        """Provide async session."""
        async with VaultSession(vault_engine=vault_engine).begin() as session:
            yield session
