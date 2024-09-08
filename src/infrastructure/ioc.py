"""Subscription provider (DI)."""

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

from src.application.interfaces.repositories.api_key import ICreateApiKeyRepository
from src.application.interfaces.repositories.api_key import IGetAPIKeysAlchemyRepository
from src.application.interfaces.repositories.api_key import IGetUserByApiKeyRepository
from src.application.interfaces.repositories.database import (
    IDropDatabaseTablesRepository,
)
from src.application.interfaces.repositories.fixture_loaders import (
    IEntityFixtureRepository,
)
from src.application.interfaces.repositories.seed import ISeedRepository
from src.application.interfaces.services.api_key import ICreateAPIKeyVaultRepository
from src.application.interfaces.services.api_key import IGetAPIKeysVaultRepository
from src.domain.entities.subscriptions import SubscriptionPlan
from src.domain.entities.users import User
from src.infrastructure.database.repositories.auth.api_key import ApiKeyRepository
from src.infrastructure.database.repositories.core.drop_database_tables import (
    DropDatabaseTablesRepository,
)
from src.infrastructure.database.repositories.subscriptions.subscription_plan import (
    SubscriptionPlanRepository,
)
from src.infrastructure.database.repositories.users.user import UserRepository
from src.infrastructure.disk.repositories.fixture_loaders import (
    SubscriptionPlanFixtureRepository,
)
from src.infrastructure.disk.repositories.fixture_loaders import UserFixtureRepository
from src.infrastructure.interfaces.uow import IDatabaseSession
from src.infrastructure.interfaces.uow import IVaultSession
from src.infrastructure.vault.base import VaultSession
from src.infrastructure.vault.repositories.api_key import ApiKeyVaultRepository
from src.main.config.settings import AppSettings
from src.main.config.settings import Settings
from src.main.config.settings import VaultSettings


class InfrastructureProvider(Provider):
    """Subscription provider (DI)."""

    settings = from_context(provides=Settings, scope=Scope.APP)
    async_engine = from_context(provides=AsyncEngine, scope=Scope.APP)
    redis_engine = from_context(provides=RedisEngine, scope=Scope.APP)
    vault_engine = from_context(provides=VaultEngine, scope=Scope.APP)

    subscription_plan_fixture_repository = provide(
        source=SubscriptionPlanFixtureRepository,
        scope=Scope.REQUEST,
        provides=IEntityFixtureRepository[SubscriptionPlan],
    )

    user_fixture_repository = provide(
        source=UserFixtureRepository,
        scope=Scope.REQUEST,
        provides=IEntityFixtureRepository[User],
    )

    user_repository = provide(
        source=UserRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[
            ISeedRepository[User],
            IGetUserByApiKeyRepository,
        ],
    )

    subscription_plan_repository = provide(
        source=SubscriptionPlanRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[ISeedRepository[SubscriptionPlan]],
    )

    drop_database_tables_repository = provide(
        source=DropDatabaseTablesRepository,
        scope=Scope.REQUEST,
        provides=IDropDatabaseTablesRepository,
    )

    api_key_repository = provide(
        source=ApiKeyRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[ICreateApiKeyRepository, IGetAPIKeysAlchemyRepository],
    )

    vault_repository = provide(
        source=ApiKeyVaultRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[ICreateAPIKeyVaultRepository, IGetAPIKeysVaultRepository],
    )

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
