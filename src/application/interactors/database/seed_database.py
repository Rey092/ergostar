"""Seed database interactor."""

import logging
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interactor import Interactor
from src.application.interfaces.services.fixture_loader import (
    IFixtureDatabaseLoaderService,
)
from src.domain.entities.subscriptions import SubscriptionPlan
from src.domain.entities.users.user import User
from src.domain.enums.database import DatabaseSeedingGroups
from src.domain.enums.database import FixtureLoadingStrategy

logger = logging.getLogger(__name__)


@dataclass
class SeedDatabaseRequestModel:
    """Seed database input data."""

    groups: list[DatabaseSeedingGroups]
    loading_strategy: FixtureLoadingStrategy = FixtureLoadingStrategy.SKIP


class SeedDatabaseInteractor(Interactor[SeedDatabaseRequestModel, None]):
    """Seed database interactor."""

    def __init__(
        self,
        session: AsyncSession,
        user_loader: IFixtureDatabaseLoaderService[User],
        subscription_plan_loader: IFixtureDatabaseLoaderService[SubscriptionPlan],
    ):
        """Initialize interactor."""
        self._session = session
        self._user_loader = user_loader
        self._subscription_plan_loader = subscription_plan_loader
        self._message_already_seeded = "{fixture_name} already seeded."

    async def __call__(
        self,
        request_model: SeedDatabaseRequestModel,
    ) -> None:
        """Seed database."""
        if DatabaseSeedingGroups.subscriptions in request_model.groups:
            logger.info("Seeding landing...")
            await self._subscription_plan_loader.load_to_database(
                fixture_name="subscription_plans",
                loading_strategy=request_model.loading_strategy,
            )
            logger.info("Landing seeded.")
        if DatabaseSeedingGroups.users in request_model.groups:
            logger.info("Seeding users...")
            await self._user_loader.load_to_database(
                fixture_name="users",
                loading_strategy=request_model.loading_strategy,
            )
            logger.info("Users seeded.")
        await self._session.commit()
