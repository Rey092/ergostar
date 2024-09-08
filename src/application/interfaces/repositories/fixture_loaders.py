"""Fixture loader interfaces."""

from abc import abstractmethod
from collections.abc import Sequence
from typing import Any
from typing import Protocol

from src.domain.common.types import EntityT


class IFixtureLoaderRepository(Protocol):
    """Load fixtures to the database."""

    @abstractmethod
    async def load_fixture(
        self,
        fixture_name: str,
    ) -> list[dict[str, Any]]:
        """Load fixture data to a dictionary."""
        ...


class IEntityFixtureRepository(IFixtureLoaderRepository, Protocol[EntityT]):
    """Load fixtures to the database."""

    entity_class: type[EntityT]

    @abstractmethod
    async def load_fixture_to_entity(
        self,
        fixture_name: str,
    ) -> Sequence[EntityT]:
        """Load fixture data to entity class."""
        ...
