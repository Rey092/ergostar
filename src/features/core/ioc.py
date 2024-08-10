"""Core provider module."""

from dishka import AnyOf
from dishka import Provider
from dishka import Scope
from dishka import provide

from src.common.interfaces.fixture_loader import IFixtureDatabaseLoader
from src.common.interfaces.fixture_loader_repository import ISeedManyEntries
from src.features.core.interactors.drop_database_tables import DropDatabaseTablesUseCase
from src.features.core.interactors.seed_database import SeedDatabaseUseCase
from src.features.core.repositories.subscription_plan import (
    SubscriptionPlanRepositoryAdapter,
)
from src.features.core.repositories.user import UserRepositoryAdapter
from src.features.core.services.fixture_loaders import (
    SubscriptionPlanFixtureDatabaseLoaderService,
)
from src.features.core.services.fixture_loaders import UserFixtureDatabaseLoaderService
from src.features.subscriptions.entities import SubscriptionPlan
from src.features.users.entities import User


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

    subscription_plan_repository = provide(
        source=SubscriptionPlanRepositoryAdapter,
        scope=Scope.REQUEST,
        provides=AnyOf[ISeedManyEntries[SubscriptionPlan]],
    )

    user_repository = provide(
        source=UserRepositoryAdapter,
        scope=Scope.REQUEST,
        provides=AnyOf[ISeedManyEntries[User]],
    )

    subscription_plan_fixture_database_loader_service = provide(
        source=SubscriptionPlanFixtureDatabaseLoaderService,
        scope=Scope.REQUEST,
        provides=IFixtureDatabaseLoader[SubscriptionPlan],
    )

    user_fixture_database_loader_service = provide(
        source=UserFixtureDatabaseLoaderService,
        scope=Scope.REQUEST,
        provides=IFixtureDatabaseLoader[User],
    )
