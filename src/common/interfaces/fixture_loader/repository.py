"""Core services interfaces."""

from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from src.common.types import EntityT


class ISeedRepository(Protocol[EntityT]):
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
