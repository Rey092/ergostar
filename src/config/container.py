"""Dependency container for the applications."""

from dishka import AsyncContainer
from dishka import make_async_container
from hvac import Client as VaultEngine
from redis.asyncio import Redis as RedisEngine
from sqlalchemy.ext.asyncio import AsyncEngine

from src.common.ioc import BasicProvider
from src.config.settings import Settings
from src.features.auth.ioc import AuthProvider
from src.features.core.ioc import CoreProvider
from src.features.subscriptions.ioc import SubscriptionsProvider
from src.features.users.ioc import UserProvider


def get_async_container(
    settings: Settings,
    alchemy_engine: AsyncEngine,
    redis_engine: RedisEngine,
    vault_engine: VaultEngine,
) -> AsyncContainer:
    """Get dependency container."""
    return make_async_container(
        CoreProvider(),
        BasicProvider(),
        SubscriptionsProvider(),
        UserProvider(),
        AuthProvider(),
        context={
            Settings: settings,
            AsyncEngine: alchemy_engine,
            RedisEngine: redis_engine,
            VaultEngine: vault_engine,
        },
    )
