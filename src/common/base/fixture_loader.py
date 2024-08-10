"""Fixture loader service."""

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

import aiofiles

from src.common.base.service import Service
from src.common.interfaces.fixture_loader import EntityT
from src.common.interfaces.fixture_loader import FuturesT
from src.common.interfaces.fixture_loader import IFixtureDatabaseLoader
from src.common.interfaces.fixture_loader import IFixtureEntityLoader
from src.common.interfaces.fixture_loader import IFixtureLoader
from src.common.interfaces.fixture_loader_repository import ISeedManyEntries
from src.config.settings import AppSettings
from src.features.core.enums import FixtureLoadingStrategy

if TYPE_CHECKING:
    from src.common.base.entity import Entity

logger = logging.getLogger(__name__)


class FixtureLoaderService(
    IFixtureLoader,
    Service,
):
    """Fixture loader service."""

    future_name: FuturesT

    def __init__(
        self,
        app_settings: AppSettings,
    ):
        """Initialize service."""
        self.features_path: str = app_settings.FEATURES_PATH

    async def load_fixture(
        self,
        fixture_name: str,
    ) -> list[dict[str, Any]]:
        """Load fixture data."""
        # prepare a fixture path
        fixture_path = (
            f"{self.features_path}/{self.future_name}/fixtures/{fixture_name}.json"
        )

        # check if fixture exists
        if not Path(fixture_path).exists():
            return []

        # load fixture data
        async with aiofiles.open(fixture_path, mode="r") as file:
            data: dict | list = json.loads(await file.read())

        return data if isinstance(data, list) else [data]


class FixtureEntityLoaderService(
    IFixtureEntityLoader[EntityT],
    FixtureLoaderService,
):
    """Fixture entity loader service."""

    entity_class: type[EntityT]
    future_name: FuturesT

    async def load_fixture_to_entity(
        self,
        fixture_name: str,
    ) -> list[EntityT]:
        """Load fixture data to dataclass."""
        # load fixture data
        fixture_data: list[dict[str, Any]] = await self.load_fixture(
            fixture_name=fixture_name,
        )

        return [self.entity_class.from_dict(data) for data in fixture_data]


class FixtureDatabaseLoaderService(
    IFixtureDatabaseLoader[EntityT],
    FixtureEntityLoaderService[EntityT],
):
    """Fixture database loader service."""

    entity_class: type[EntityT]
    future_name: FuturesT

    def __init__(
        self,
        app_settings: AppSettings,
        repository: ISeedManyEntries[EntityT],
    ):
        """Initialize service."""
        super().__init__(app_settings=app_settings)
        self._repository = repository
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

    async def load_to_database(
        self,
        fixture_name: str,
        loading_strategy: FixtureLoadingStrategy,
    ) -> None:
        """Load many entities."""
        # check if loading is allowed
        if not await self._is_loading_allowed(
            fixture_name=fixture_name,
            loading_exists_strategy=loading_strategy,
        ):
            return

        # load entities
        entities: list[Entity] = await self.load_fixture_to_entity(
            fixture_name=fixture_name,
        )

        # add entities
        await self._repository.add_many(data=entities)

        logger.info(self._message_success.format(fixture_name=fixture_name))

    async def _is_loading_allowed(
        self,
        fixture_name: str,
        loading_exists_strategy: FixtureLoadingStrategy,
    ) -> bool:
        """Check if loading is allowed.

        Returns True if loading is allowed, otherwise False.
        """
        # skip loading if strategy is ALLOW
        if loading_exists_strategy == FixtureLoadingStrategy.ALLOW:
            logger.info(self._message_allowed.format(fixture_name=fixture_name))
            return True

        # if no data exists, allow loading
        if not await self._repository.exists_anything():
            logger.info(self._message_not_exists.format(fixture_name=fixture_name))
            return True

        # skip loading if data exists and strategy is SKIP
        if loading_exists_strategy == FixtureLoadingStrategy.SKIP:
            logger.info(self._message_skip.format(fixture_name=fixture_name))
            return False

        # delete all data if data exists and strategy is OVERRIDE
        if loading_exists_strategy == FixtureLoadingStrategy.OVERRIDE:
            logger.info(self._message_override.format(fixture_name=fixture_name))
            await self._repository.delete_everything()
            return True

        # if strategy is RAISE
        if loading_exists_strategy == FixtureLoadingStrategy.RAISE:
            raise ValueError(
                self._exception_already_seeded.format(fixture_name=fixture_name),
            )

        raise ValueError(self._exception_invalid_strategy)
