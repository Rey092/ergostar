"""Seed database interactor."""

import logging
from dataclasses import dataclass

from admin.core.enums import DatabaseSeedingGroups
from src.common.base.use_case import UseCase
from src.common.interfaces.db import IDatabaseSession
from src.features.core.enums import FixtureLoadingStrategy
from src.features.core.services import interfaces as services_interfaces
from src.features.core.use_cases import interfaces as use_case_interfaces
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
        session: IDatabaseSession,
        fixture_loader_service: use_case_interfaces.ILoadFixturesToDatabase,
        subscription_plan_gateway: services_interfaces.ISeedManySubscriptionPlanEntries,
        users_gateway: services_interfaces.ISeedManyUserEntries,
    ):
        """Initialize interactor."""
        self._session = session
        self._fixture_loader_service = fixture_loader_service
        self._subscription_plan_gateway = subscription_plan_gateway
        self._users_gateway = users_gateway
        self._message_already_seeded = "{fixture_name} already seeded."

    async def __call__(
        self,
        request_model: SeedDatabaseRequestModel,
        **kwargs,
    ) -> None:
        """Seed database."""
        if DatabaseSeedingGroups.subscriptions in request_model.groups:
            logger.info("Seeding landing...")
            await self._fixture_loader_service.load_fixture_to_database(
                future_name="subscriptions",
                fixture_name="subscription_plans",
                entity_class=SubscriptionPlan,
                gateway=self._subscription_plan_gateway,
                loading_strategy=request_model.loading_strategy,
            )
            logger.info("Landing seeded.")

        logger.info("Seeding users...")
        await self._fixture_loader_service.load_fixture_to_database(
            future_name="users",
            fixture_name="users",
            entity_class=User,
            gateway=self._users_gateway,
            loading_strategy=request_model.loading_strategy,
        )
        logger.info("Users seeded.")

        await self._session.commit()
