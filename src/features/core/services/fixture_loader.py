"""Fixture loader service."""

import json
import logging
from enum import Enum
from pathlib import Path
from typing import Any
from typing import TypeVar

import aiofiles

from src.common.base.entity import Entity
from src.config.settings import AppSettings
from src.features.core.interactors.interfaces import ISeedManyEntries

T = TypeVar("T", bound=Entity)
logger = logging.getLogger(__name__)


class FixtureLoadingStrategy(Enum):
    """Loading exists mode.

    SKIP: Skip loading if it already exists.
    OVERRIDE: Override data if already
    RAISE: Raise an error if already exists.
    """

    SKIP = "skip"
    OVERRIDE = "override"
    RAISE = "raise"


class FixtureLoaderService:
    """Fixture loader service."""

    def __init__(
        self,
        app_settings: AppSettings,
    ):
        """Initialize service."""
        self.features_path: str = app_settings.FEATURES_PATH
        self._message_success = "{fixture_name} seeded successfully."
        self._message_allowed = "{fixture_name} is allowed to seed."
        self._message_skip = "{fixture_name} already seeded. Skipping."
        self._message_override = "{fixture_name} already seeded. Overriding."
        self._exception_already_seeded = (
            "{fixture_name} already seeded. Raising an error."
        )
        self._exception_invalid_strategy = "Invalid loading strategy."

    async def load_fixture(
        self,
        future_name: str,
        fixture_name: str,
    ) -> list[dict[str, Any]]:
        """Load fixture data."""
        # prepare a fixture path
        fixture_path = (
            f"{self.features_path}/{future_name}/fixtures/{fixture_name}.json"
        )

        # check if fixture exists
        if not Path(fixture_path).exists():
            return []

        # load fixture data
        async with aiofiles.open(fixture_path, mode="r") as file:
            data: dict | list = json.loads(await file.read())

        return data if isinstance(data, list) else [data]

    async def load_fixture_to_entity(
        self,
        future_name: str,
        fixture_name: str,
        entity_class: type[Entity],
    ) -> list[Entity]:
        """Load fixture data to dataclass."""
        # load fixture data
        fixture_data: list[dict[str, Any]] = await self.load_fixture(
            future_name=future_name,
            fixture_name=fixture_name,
        )

        return [entity_class.from_dict(data) for data in fixture_data]

    async def load_fixture_to_database(
        self,
        future_name: str,
        fixture_name: str,
        entity_class: type[Entity],
        repository: ISeedManyEntries,
        loading_exists_strategy: FixtureLoadingStrategy = FixtureLoadingStrategy.SKIP,
    ) -> None:
        """Load many entities."""
        # check if loading is allowed
        if not await self._is_loading_allowed(
            fixture_name=fixture_name,
            repository=repository,
            loading_exists_strategy=loading_exists_strategy,
        ):
            return

        # load entities
        entities: list[Entity] = await self.load_fixture_to_entity(
            future_name=future_name,
            fixture_name=fixture_name,
            entity_class=entity_class,
        )

        # add entities
        await repository.add_many(data=entities)

        logger.info(self._message_success.format(fixture_name=fixture_name))

    async def _is_loading_allowed(
        self,
        fixture_name: str,
        repository: ISeedManyEntries,
        loading_exists_strategy: FixtureLoadingStrategy,
    ) -> bool:
        """Check if loading is allowed.

        Returns True if loading is allowed, otherwise False.
        """
        # if no data exists, allow loading
        if not await repository.exists():
            logger.info(self._message_allowed.format(fixture_name=fixture_name))
            return True

        # skip loading if data exists and strategy is SKIP
        if loading_exists_strategy == FixtureLoadingStrategy.SKIP:
            logger.info(self._message_skip.format(fixture_name=fixture_name))
            return False

        # delete all data if data exists and strategy is OVERRIDE
        if loading_exists_strategy == FixtureLoadingStrategy.OVERRIDE:
            logger.info(self._message_override.format(fixture_name=fixture_name))
            await repository.delete_all()
            return True

        # if strategy is RAISE
        if loading_exists_strategy == FixtureLoadingStrategy.RAISE:
            raise ValueError(
                self._exception_already_seeded.format(fixture_name=fixture_name),
            )

        raise ValueError(self._exception_invalid_strategy)
