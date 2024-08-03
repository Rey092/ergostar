"""Seed database interactor."""

import logging

from src.common.interfaces.db import IDatabaseSession
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
