"""Seed database interactor."""

import logging
from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from src.common.base.entity import Entity
from src.common.base.use_case import UseCase
from src.common.interfaces.db import IDatabaseSession
from src.features.core.enums import FixtureLoadingStrategy
from src.features.core.services.fixture_loader import ISeedManyEntries
from unfold.core.enums import DatabaseSeedingGroups

logger = logging.getLogger(__name__)


class ILoadFixturesToDatabase(Protocol):
    """Load fixtures to the database."""

    @abstractmethod
    async def load_fixture_to_database(
        self,
        future_name: str,
        fixture_name: str,
        entity_class: type[Entity],
        repository: ISeedManyEntries,
        loading_strategy: FixtureLoadingStrategy,
    ) -> None:
        """Load many entities."""
        ...


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
        fixture_loader_service: ILoadFixturesToDatabase,
        *args,
    ):
        """Initialize interactor."""
        super().__init__(*args)
        self._session = session
        self._fixture_loader_service = fixture_loader_service
        self._message_already_seeded = "{fixture_name} already seeded."

    async def __call__(
        self,
        request_model: SeedDatabaseRequestModel,
        **kwargs,
    ) -> None:
        """Seed database."""
        if DatabaseSeedingGroups.subscriptions in request_model.groups:
            logger.info("Seeding landing...")
            logger.info("Landing seeded.")

        await self._session.commit()
