"""Core services interfaces."""

from abc import abstractmethod
from collections.abc import Sequence
from typing import Any
from typing import Protocol
from typing import TypeVar

from src.features.subscriptions.entities import SubscriptionPlan
from src.features.users.entities import User

ModelT = TypeVar("ModelT", bound=Any)


class ISeedCheckExists(Protocol):
    """ISeedCheckExists."""

    @abstractmethod
    async def exists_anything(self) -> bool:
        """Check if entry exists."""
        ...


class ISeedManyEntries(ISeedCheckExists, Protocol[ModelT]):
    """ISeedManyEntries."""

    @abstractmethod
    async def add_many(self, data: list[ModelT]) -> Sequence[ModelT]:
        """Add many entries."""
        ...

    @abstractmethod
    async def delete_everything(self) -> None:
        """Delete all entries."""
        ...


class ISeedManySubscriptionPlanEntries(ISeedManyEntries[SubscriptionPlan], Protocol):
    """ISeedManySubscriptionPlanEntries."""


class ISeedManyUserEntries(ISeedManyEntries[User], Protocol):
    """ISeedManyUserEntries."""
