"""Dependency container for the applications."""

from dishka import AsyncContainer
from dishka import make_async_container
from hvac import Client as VaultEngine
from redis.asyncio import Redis as RedisEngine
from sqlalchemy.ext.asyncio import AsyncEngine

from src.application.ioc import ApplicationProvider
from src.infrastructure.ioc import InfrastructureProvider
from src.main.config.settings import Settings


def get_async_container(
    settings: Settings,
    alchemy_engine: AsyncEngine,
    redis_engine: RedisEngine,
    vault_engine: VaultEngine,
) -> AsyncContainer:
    """Get dependency container."""
    return make_async_container(
        InfrastructureProvider(),
        ApplicationProvider(),
        context={
            Settings: settings,
            AsyncEngine: alchemy_engine,
            RedisEngine: redis_engine,
            VaultEngine: vault_engine,
        },
    )
