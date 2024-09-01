"""Core provider module."""

from dishka import AnyOf
from dishka import Provider
from dishka import Scope
from dishka import provide

from src.common.interfaces.fixture_loader.repository import ISeedRepository
from src.common.interfaces.fixture_loader.service import IFixtureDatabaseLoader
from src.features.core.interactors.drop_database_tables import (
    DropDatabaseTablesInteractor,
)
from src.features.core.interactors.seed_database import SeedDatabaseInteractor
from src.features.core.interfaces.repositories import IDropDatabaseTablesRepository
from src.features.core.public.interfaces import IGenerateUUID7Service
from src.features.core.repositories.a_subscription_plan import (
    SubscriptionPlanRepository,
)
from src.features.core.repositories.a_user import UserRepository
from src.features.core.repositories.drop_database_tables import (
    DropDatabaseTablesRepository,
)
from src.features.core.services.fixture_loaders import (
    SubscriptionPlanFixtureDatabaseLoaderService,
)
from src.features.core.services.fixture_loaders import UserFixtureDatabaseLoaderService
from src.features.core.services.uuid_generator import UUIDGeneratorService
from src.features.subscriptions.public.entities import SubscriptionPlanEntity
from src.features.users.public.entities import UserEntity


class CoreProvider(Provider):
    """Core provider (DI)."""

    drop_database_tables_interactor = provide(
        source=DropDatabaseTablesInteractor,
        scope=Scope.REQUEST,
    )

    seed_database_interactor = provide(
        source=SeedDatabaseInteractor,
        scope=Scope.REQUEST,
    )

    subscription_plan_repository = provide(
        source=SubscriptionPlanRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[ISeedRepository[SubscriptionPlanEntity]],
    )

    user_repository = provide(
        source=UserRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[ISeedRepository[UserEntity]],
    )

    drop_database_tables_repository = provide(
        source=DropDatabaseTablesRepository,
        scope=Scope.REQUEST,
        provides=IDropDatabaseTablesRepository,
    )

    subscription_plan_fixture_database_loader_service = provide(
        source=SubscriptionPlanFixtureDatabaseLoaderService,
        scope=Scope.REQUEST,
        provides=IFixtureDatabaseLoader[SubscriptionPlanEntity],
    )

    user_fixture_database_loader_service = provide(
        source=UserFixtureDatabaseLoaderService,
        scope=Scope.REQUEST,
        provides=IFixtureDatabaseLoader[UserEntity],
    )

    uuid_generator_service = provide(
        source=UUIDGeneratorService,
        scope=Scope.APP,
        provides=IGenerateUUID7Service,
    )
