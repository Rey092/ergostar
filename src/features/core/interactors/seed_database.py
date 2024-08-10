"""Seed database interactor."""

import logging
from dataclasses import dataclass

from admin.core.enums import DatabaseSeedingGroups
from src.common.base.interactor import UseCase
from src.common.interfaces.database_session import IAlchemySession
from src.common.interfaces.fixture_loader import IFixtureDatabaseLoader
from src.features.core.enums import FixtureLoadingStrategy
from src.features.subscriptions.entities import SubscriptionPlan
from src.features.users.entities import User

logger = logging.getLogger(__name__)


@dataclass
class SeedDatabaseRequestModel:
    """Seed database input data."""

    groups: list[DatabaseSeedingGroups]
    loading_strategy: FixtureLoadingStrategy = FixtureLoadingStrategy.SKIP


class SeedDatabaseUseCase(UseCase[SeedDatabaseRequestModel, None]):
    """Seed database use case."""

    def __init__(
        self,
        session: IAlchemySession,
        subscription_plan_fixture_database_loader_service: IFixtureDatabaseLoader[
            SubscriptionPlan
        ],
        user_fixture_database_loader_service: IFixtureDatabaseLoader[User],
    ):
        """Initialize interactor."""
        self._session = session
        self._subscription_plan_fixture_loader_service = (
            subscription_plan_fixture_database_loader_service
        )
        self._user_fixture_database_loader_service = (
            user_fixture_database_loader_service
        )
        self._message_already_seeded = "{fixture_name} already seeded."

    async def __call__(
        self,
        request_model: SeedDatabaseRequestModel,
        **kwargs,
    ) -> None:
        """Seed database."""
        if DatabaseSeedingGroups.subscriptions in request_model.groups:
            logger.info("Seeding landing...")
            await self._subscription_plan_fixture_loader_service.load_to_database(
                fixture_name="subscription_plans",
                loading_strategy=request_model.loading_strategy,
            )
            logger.info("Landing seeded.")

        if DatabaseSeedingGroups.users in request_model.groups:
            logger.info("Seeding users...")
            await self._subscription_plan_fixture_loader_service.load_to_database(
                fixture_name="users",
                loading_strategy=request_model.loading_strategy,
            )
            logger.info("Users seeded.")

        await self._session.commit()
