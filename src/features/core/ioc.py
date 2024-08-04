"""Core provider module."""

from dishka import AnyOf
from dishka import Provider
from dishka import Scope
from dishka import provide

from src.features.core.gateways.adapters.subscription_plan import (
    SubscriptionPlanGatewayAdapter,
)
from src.features.core.gateways.adapters.user import UserGatewayAdapter
from src.features.core.services.fixture_loader import FixtureLoaderService
from src.features.core.services.interfaces import ISeedManySubscriptionPlanEntries
from src.features.core.services.interfaces import ISeedManyUserEntries
from src.features.core.use_cases.drop_database_tables import DropDatabaseTablesUseCase
from src.features.core.use_cases.interfaces import ILoadFixturesToDatabase
from src.features.core.use_cases.seed_database import SeedDatabaseUseCase


class CoreProvider(Provider):
    """Core provider (DI)."""

    drop_database_interactor = provide(
        source=DropDatabaseTablesUseCase,
        scope=Scope.REQUEST,
    )

    seed_database_interactor = provide(
        source=SeedDatabaseUseCase,
        scope=Scope.REQUEST,
    )

    fixture_loader_service = provide(
        source=FixtureLoaderService,
        scope=Scope.REQUEST,
        provides=AnyOf[ILoadFixturesToDatabase],
    )

    subscription_plan_gateway = provide(
        source=SubscriptionPlanGatewayAdapter,
        scope=Scope.REQUEST,
        provides=AnyOf[ISeedManySubscriptionPlanEntries],
    )

    users_gateway = provide(
        source=UserGatewayAdapter,
        scope=Scope.REQUEST,
        provides=AnyOf[ISeedManyUserEntries],
    )
