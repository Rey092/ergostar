"""Common repository implementations."""

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any
from typing import cast

import aiofiles

from src.application.interfaces.repositories.fixture_loaders import (
    IEntityFixtureRepository,
)
from src.application.interfaces.repositories.fixture_loaders import (
    IFixtureLoaderRepository,
)
from src.domain.common.types import EntityT
from src.main.config.settings import AppSettings


class FixtureLoaderRepository(
    IFixtureLoaderRepository,
):
    """Fixture loader service."""

    def __init__(
        self,
        app_settings: AppSettings,
    ):
        """Initialize service."""
        self.fixtures_path: str = app_settings.FIXTURES_PATH
        self._message_not_found = "Fixture {fixture_name} not found."

    async def load_fixture(
        self,
        fixture_name: str,
    ) -> list[dict[str, Any]]:
        """Load fixture data."""
        fixture_path = f"{self.fixtures_path}/{fixture_name}.json"

        if not Path(fixture_path).exists():
            raise FileNotFoundError(
                self._message_not_found.format(fixture_name=fixture_name),
            )

        async with aiofiles.open(fixture_path, mode="r") as file:
            data: dict | list = json.loads(await file.read())

        return data if isinstance(data, list) else [data]


class EntityFixtureRepository(
    FixtureLoaderRepository,
    IEntityFixtureRepository[EntityT],
):
    """Fixture entity loader service."""

    entity_class: type[EntityT]

    def __init__(self, app_settings: AppSettings):
        """Initialize service."""
        super().__init__(app_settings=app_settings)

    async def load_fixture_to_entity(
        self,
        fixture_name: str,
    ) -> Sequence[EntityT]:
        """Load fixture data to dataclass."""
        fixture_data: list[dict[str, Any]] = await self.load_fixture(
            fixture_name=fixture_name,
        )

        return [
            cast(EntityT, self.entity_class.from_dict(data)) for data in fixture_data
        ]
