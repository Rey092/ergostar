"""Interfaces for Landing Home Page Repositories."""

from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from typing import TypeVar

from src.common.base.entity import Entity

ModelT = TypeVar("ModelT", bound=Entity)


class ISeedCheckExists(Protocol):
    """ISeedCheckExists."""

    @abstractmethod
    async def exists(self) -> bool:
        """Check if entry exists."""
        ...


class ISeedOneEntry(ISeedCheckExists, Protocol[ModelT]):
    """ISeedOneEntry."""

    @abstractmethod
    async def add(self, data: ModelT) -> ModelT:
        """Add one entry."""
        ...


class ISeedManyEntries(ISeedCheckExists, Protocol[ModelT]):
    """ISeedManyEntries."""

    @abstractmethod
    async def add_many(self, data: list[ModelT]) -> Sequence[ModelT]:
        """Add many entries."""
        ...
