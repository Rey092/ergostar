"""Interfaces for core use cases."""

from abc import abstractmethod
from typing import Any
from typing import Literal
from typing import Protocol
from typing import TypeVar

from src.common.base.entity import Entity
from src.features.core.enums import FixtureLoadingStrategy

EntityT = TypeVar("EntityT", bound=Entity)
FuturesT = Literal["auth", "core", "subscriptions", "users"]


class IFixtureLoader(Protocol):
    """Load fixtures to the database."""

    future_name: FuturesT

    @abstractmethod
    async def load_fixture(
        self,
        fixture_name: str,
    ) -> list[dict[str, Any]]:
        """Load fixture data to a dictionary."""
        ...


class IFixtureEntityLoader(IFixtureLoader, Protocol[EntityT]):
    """Load fixtures to the database."""

    entity_class: type[EntityT]
    future_name: FuturesT

    @abstractmethod
    async def load_fixture_to_entity(
        self,
        fixture_name: str,
    ) -> list[EntityT]:
        """Load fixture data to entity class."""
        ...


class IFixtureDatabaseLoader(
    IFixtureEntityLoader[EntityT],
    Protocol[EntityT],
):
    """Load fixtures to the database."""

    entity_class: type[EntityT]
    future_name: FuturesT

    @abstractmethod
    async def load_to_database(
        self,
        fixture_name: str,
        loading_strategy: FixtureLoadingStrategy,
    ) -> None:
        """Load fixture data to the database."""
        ...
