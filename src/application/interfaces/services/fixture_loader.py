"""Fixture loader interfaces."""

from abc import abstractmethod
from collections.abc import Sequence
from typing import Any
from typing import Protocol

from src.domain.common.types import EntityT
from src.domain.enums.database import FixtureLoadingStrategy


class IFixtureLoaderService(Protocol):
    """Load fixtures to the database."""

    @abstractmethod
    async def load_fixture(
        self,
        fixture_name: str,
    ) -> list[dict[str, Any]]:
        """Load fixture data to a dictionary."""
        ...


class IFixtureEntityLoaderService(IFixtureLoaderService, Protocol[EntityT]):
    """Load fixtures to the database."""

    entity_class: type[EntityT]

    @abstractmethod
    async def load_fixture_to_entity(
        self,
        fixture_name: str,
    ) -> Sequence[EntityT]:
        """Load fixture data to entity class."""
        ...


class IFixtureDatabaseLoaderService(
    IFixtureEntityLoaderService[EntityT],
    Protocol[EntityT],
):
    """Load fixtures to the database."""

    entity_class: type[EntityT]

    @abstractmethod
    async def load_to_database(
        self,
        fixture_name: str,
        loading_strategy: FixtureLoadingStrategy,
    ) -> None:
        """Load fixture data to the database."""
        ...
