"""Common interfaces for infrastructure layer."""

from abc import ABC
from abc import abstractmethod
from typing import Protocol


class ISession(Protocol):
    """Session interface."""

    @abstractmethod
    async def commit(self) -> None:
        """Commit the transaction."""
        ...

    @abstractmethod
    async def flush(self) -> None:
        """Flush the session."""
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the transaction."""
        ...


class IDatabaseSession(ISession, ABC):
    """IDatabaseSession protocol."""


class IVaultSession(ISession, ABC):
    """IVaultSession protocol."""


class IRepository:
    """Repository interface."""

    _session: ISession
