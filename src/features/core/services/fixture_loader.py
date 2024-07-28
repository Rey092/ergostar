"""Fixture loader service."""
import json
from typing import Any, Type, TypeVar

import aiofiles
from pathlib import Path

from src.common.base.entity import Entity
from src.common.types import SETTINGS_FEATURES_PATH


T = TypeVar('T', bound=Entity)


class FixtureLoaderService:
    """Fixture loader service."""

    def __init__(
        self,
        features_path: SETTINGS_FEATURES_PATH,
    ):
        """Initialize service."""
        self.features_path = features_path

    async def load_fixture(
        self,
        future_name: str,
        fixture_name: str
    ) -> list[dict[str, Any]]:
        """Load fixture data."""
        # prepare a fixture path
        fixture_path = f"{self.features_path}/{future_name}/fixtures/{fixture_name}.json"

        # check if fixture exists
        if not Path(fixture_path).exists():
            return []

        # load fixture data
        async with aiofiles.open(fixture_path, mode="r") as file:
            contents = await file.read()
            data: dict | list = json.loads(contents)

        # check if data is a dictionary
        if isinstance(data, dict):
            data = [data]

        return data

    async def load_fixture_to_entity(
        self,
        future_name: str,
        fixture_name: str,
        entity_class: Type[T]
    ) -> list[T]:
        """Load fixture data to dataclass."""

        # load fixture data
        fixture_data: list[dict[str, Any]] = await self.load_fixture(future_name, fixture_name)

        # check if fixture data exists
        if not fixture_data:
            return []

        # convert fixture data to dataclass objects
        dataclass_objects: list[Entity] = [
            entity_class.from_dict(data)
            for data in fixture_data
        ]

        return dataclass_objects
