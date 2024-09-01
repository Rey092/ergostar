"""Common interfaces."""

from abc import ABC
from abc import abstractmethod
from typing import Protocol


class IUnitOfWork(Protocol):
    """IUnitOfWork protocol."""

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


class IDatabaseSession(IUnitOfWork, ABC):
    """IDatabaseSession protocol."""


class IVaultSession(IUnitOfWork, ABC):
    """IVaultSession protocol."""
