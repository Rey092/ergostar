"""Auth provider module."""

from dishka import AnyOf
from dishka import Provider
from dishka import Scope
from dishka import provide

from src.application.interactors.auth.authenticate import AuthenticateApiKeyInteractor
from src.application.interactors.auth.create_api_key import CreateApiKeyInteractor
from src.application.interactors.auth.get_user_api_keys import GetUserApiKeysInteractor
from src.application.interactors.database.drop_database import DropDatabaseInteractor
from src.application.interactors.database.seed_database import SeedDatabaseInteractor
from src.application.interfaces.services.fixture_loader import (
    IFixtureDatabaseLoaderService,
)
from src.application.interfaces.services.hashers import IHasher
from src.application.interfaces.services.hashers import IHashVerifier
from src.application.interfaces.services.uuid import IGenerateUUID7Service
from src.application.services.auth.hasher_blake2b import HasherBlake2b
from src.application.services.core.fixture_loaders import (
    SubscriptionPlanFixtureDatabaseLoaderService,
)
from src.application.services.core.fixture_loaders import (
    UserFixtureDatabaseLoaderService,
)
from src.application.services.core.uuid_generator import UUIDGeneratorService
from src.domain.entities.subscriptions import SubscriptionPlan
from src.domain.entities.users import User


class ApplicationProvider(Provider):
    """Auth provider (DI)."""

    drop_database_tables_interactor = provide(
        source=DropDatabaseInteractor,
        scope=Scope.REQUEST,
    )

    seed_database_interactor = provide(
        source=SeedDatabaseInteractor,
        scope=Scope.REQUEST,
    )

    authenticate_api_key_interactor = provide(
        source=AuthenticateApiKeyInteractor,
        scope=Scope.REQUEST,
    )

    create_api_key_interactor = provide(
        source=CreateApiKeyInteractor,
        scope=Scope.REQUEST,
    )

    get_user_api_keys_interactor = provide(
        source=GetUserApiKeysInteractor,
        scope=Scope.REQUEST,
    )

    hasher_service = provide(
        source=HasherBlake2b,
        scope=Scope.APP,
        provides=AnyOf[IHasher, IHashVerifier],
    )

    subscription_plan_fixture_database_loader_service = provide(
        source=SubscriptionPlanFixtureDatabaseLoaderService,
        scope=Scope.REQUEST,
        provides=IFixtureDatabaseLoaderService[SubscriptionPlan],
    )

    user_fixture_database_loader_service = provide(
        source=UserFixtureDatabaseLoaderService,
        scope=Scope.REQUEST,
        provides=IFixtureDatabaseLoaderService[User],
    )

    uuid_generator_service = provide(
        source=UUIDGeneratorService,
        scope=Scope.APP,
        provides=IGenerateUUID7Service,
    )
