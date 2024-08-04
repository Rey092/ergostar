"""Interfaces for core use cases."""

from abc import abstractmethod
from typing import Protocol

from src.common.base.entity import Entity
from src.features.core.enums import FixtureLoadingStrategy
from src.features.core.services.interfaces import ISeedManyEntries


class ILoadFixturesToDatabase(Protocol):
    """Load fixtures to the database."""

    @abstractmethod
    async def load_fixture_to_database(
        self,
        future_name: str,
        fixture_name: str,
        entity_class: type[Entity],
        gateway: ISeedManyEntries,
        loading_strategy: FixtureLoadingStrategy,
    ) -> None:
        """Load many entities."""
        ...
