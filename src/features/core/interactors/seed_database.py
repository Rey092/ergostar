"""Seed database interactor."""

import logging

from src.common.base.entity import Entity
from src.common.interfaces.db import IDatabaseSession
from src.features.core.interactors import interfaces
from src.features.core.services.fixture_loader import FixtureLoaderService
from unfold.core.enums import DatabaseSeedingGroups

logger = logging.getLogger(__name__)


class SeedDatabaseInteractor:
    """Seed database interactor."""

    def __init__(
        self,
        session: IDatabaseSession,
        fixture_loader_service: FixtureLoaderService,
    ):
        """Initialize interactor."""
        self._session = session
        self._fixture_loader_service = fixture_loader_service
        self._message_already_seeded = "{fixture_name} already seeded."

    async def __call__(
        self,
        seeding_groups: list[DatabaseSeedingGroups],
    ) -> None:
        """Seed database."""
        if DatabaseSeedingGroups.landing in seeding_groups:
            logger.info("Seeding landing...")
            logger.info("Landing seeded.")

        await self._session.commit()

    async def _load_one_entity(
        self,
        future_name: str,
        fixture_name: str,
        entity_class: type[Entity],
        repository: interfaces.ISeedOneEntry,
    ) -> None:
        """Load one entity."""
        # check if already seeded
        if await repository.exists():
            logger.info(
                self._message_already_seeded.format(fixture_name=fixture_name),
            )
            return

        # load entities
        entities: list[
            Entity
        ] = await self._fixture_loader_service.load_fixture_to_entity(
            future_name=future_name,
            fixture_name=fixture_name,
            entity_class=entity_class,
        )

        # get the first entity
        entity: Entity = entities[0]

        # add entity
        await repository.add(data=entity)

    async def _load_many_entities(
        self,
        future_name: str,
        fixture_name: str,
        entity_class: type[Entity],
        repository: interfaces.ISeedManyEntries,
    ) -> None:
        """Load many entities."""
        # check if already seeded
        if await repository.exists():
            logger.info(
                self._message_already_seeded.format(fixture_name=fixture_name),
            )
            return

        # load entities
        entities: list[
            Entity
        ] = await self._fixture_loader_service.load_fixture_to_entity(
            future_name=future_name,
            fixture_name=fixture_name,
            entity_class=entity_class,
        )

        # add entities
        await repository.add_many(data=entities)
