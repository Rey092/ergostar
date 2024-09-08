"""Seed database interactor."""

import logging
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interactor import Interactor
from src.application.interfaces.repositories.fixture_loaders import (
    IEntityFixtureRepository,
)
from src.application.interfaces.repositories.seed import ISeedRepository
from src.domain.common.entity import Entity
from src.domain.entities.subscriptions import SubscriptionPlan
from src.domain.entities.users.user import User
from src.domain.enums.database import DatabaseSeedingGroups
from src.domain.enums.database import FixtureLoadingStrategy

logger = logging.getLogger(__name__)


@dataclass
class SeedDatabaseRequestModel:
    """Seed database input data."""

    groups: set[DatabaseSeedingGroups]
    loading_strategy: FixtureLoadingStrategy = FixtureLoadingStrategy.SKIP


class SeedDatabaseInteractor(Interactor[SeedDatabaseRequestModel, None]):
    """Seed database interactor."""

    def __init__(
        self,
        session: AsyncSession,
        user_repository: ISeedRepository[User],
        user_fixture_repository: IEntityFixtureRepository[User],
        subscription_plan_repository: ISeedRepository[SubscriptionPlan],
        subscription_plan_fixture_repository: IEntityFixtureRepository[
            SubscriptionPlan
        ],
    ):
        """Initialize interactor."""
        self._session = session
        self._message_already_seeded = "{fixture_name} already seeded."
        self._message_success = "{fixture_name} seeded successfully."
        self._message_allowed = "{fixture_name} is allowed to seed."
        self._message_not_exists = (
            "{fixture_name} is allowed to be seeded, because the table is empty."
        )
        self._message_skip = "{fixture_name} already seeded. Skipping."
        self._message_override = "{fixture_name} already seeded. Overriding."
        self._exception_already_seeded = (
            "{fixture_name} already seeded. Raising an error."
        )
        self._exception_invalid_strategy = "Invalid loading strategy."

        self._group_to_repository: dict[
            DatabaseSeedingGroups,
            ISeedRepository,
        ] = {
            DatabaseSeedingGroups.subscriptions: subscription_plan_repository,
            DatabaseSeedingGroups.users: user_repository,
        }
        self._group_to_fixture_repository: dict[
            DatabaseSeedingGroups,
            IEntityFixtureRepository,
        ] = {
            DatabaseSeedingGroups.subscriptions: subscription_plan_fixture_repository,
            DatabaseSeedingGroups.users: user_fixture_repository,
        }
        self._group_to_fixture_name: dict[DatabaseSeedingGroups, str] = {
            DatabaseSeedingGroups.subscriptions: "subscription_plans",
            DatabaseSeedingGroups.users: "users",
        }

    async def __call__(
        self,
        request_model: SeedDatabaseRequestModel,
    ) -> None:
        """Seed database."""
        for group in request_model.groups:
            await self._load_to_database(
                group=group,
                loading_strategy=request_model.loading_strategy,
            )

        await self._session.commit()

    async def _load_to_database(
        self,
        group: DatabaseSeedingGroups,
        loading_strategy: FixtureLoadingStrategy,
    ) -> None:
        """Load many entities."""
        fixture_name: str = self._group_to_fixture_name[group]
        fixture_repository: IEntityFixtureRepository[Entity] = (
            self._group_to_fixture_repository[group]
        )
        repository: ISeedRepository[Entity] = self._group_to_repository[group]

        if not await self._is_loading_allowed(
            repository=repository,
            fixture_name=fixture_name,
            loading_exists_strategy=loading_strategy,
        ):
            return

        entities: list[Entity] = list(
            await fixture_repository.load_fixture_to_entity(
                fixture_name=fixture_name,
            ),
        )

        await repository.add_many(data=entities)

        logger.info(self._message_success.format(fixture_name=fixture_name))

    async def _is_loading_allowed(
        self,
        repository: ISeedRepository[Entity],
        fixture_name: str,
        loading_exists_strategy: FixtureLoadingStrategy,
    ) -> bool:
        """Check if loading is allowed.

        Returns True if loading is allowed, otherwise False.
        """
        if loading_exists_strategy == FixtureLoadingStrategy.ALLOW:
            logger.info(self._message_allowed.format(fixture_name=fixture_name))
            return True

        if not await repository.exists_anything():
            logger.info(self._message_not_exists.format(fixture_name=fixture_name))
            return True

        if loading_exists_strategy == FixtureLoadingStrategy.SKIP:
            logger.info(self._message_skip.format(fixture_name=fixture_name))
            return False

        if loading_exists_strategy == FixtureLoadingStrategy.OVERRIDE:
            logger.info(self._message_override.format(fixture_name=fixture_name))
            await repository.delete_everything()
            return True

        if loading_exists_strategy == FixtureLoadingStrategy.RAISE:
            raise ValueError(
                self._exception_already_seeded.format(fixture_name=fixture_name),
            )

        raise ValueError(self._exception_invalid_strategy)
