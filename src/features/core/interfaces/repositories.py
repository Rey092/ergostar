"""Repository interfaces."""

from abc import abstractmethod
from typing import Protocol


class IDropDatabaseTablesRepository(Protocol):
    """Drop database tables repository interface."""

    @abstractmethod
    async def drop_database_tables(self) -> None:
        """Drop database tables."""
        ...
