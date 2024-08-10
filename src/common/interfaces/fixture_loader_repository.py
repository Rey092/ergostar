"""Core services interfaces."""

from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from typing import TypeVar

from src.common.base.entity import Entity

EntityT = TypeVar("EntityT", bound=Entity)


class ISeedManyEntries(Protocol[EntityT]):
    """ISeedManyEntries."""

    @abstractmethod
    async def exists_anything(self) -> bool:
        """Check if entry exists."""
        ...

    @abstractmethod
    async def add_many(self, data: list[EntityT]) -> Sequence[EntityT]:
        """Add many entries."""
        ...

    @abstractmethod
    async def delete_everything(self) -> None:
        """Delete all entries."""
        ...
