"""Common interfaces."""
from abc import abstractmethod
from collections.abc import Iterable
from typing import Any
from typing import Protocol
from typing import TypeVar

from sqlalchemy import Executable
from sqlalchemy import Result

# noinspection PyProtectedMember
from sqlalchemy.engine.interfaces import _CoreAnyExecuteParams
from sqlalchemy.sql.selectable import ForUpdateParameter

_T = TypeVar("_T", bound=Any)


class IDatabaseSession(Protocol):
    """IDatabaseSession protocol."""

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


class IAlchemySession(IDatabaseSession, Protocol):
    """IAlchemySession protocol."""

    async def execute(
        self,
        statement: Executable,
        params: _CoreAnyExecuteParams | None = None,
    ) -> Result[_T]:
        """Execute the given statement."""
        ...

    async def refresh(
        self,
        instance: object,
        attribute_names: Iterable[str] | None = None,
        with_for_update: ForUpdateParameter = None,
    ) -> None:
        """Refresh the given instance with the most recent state from the database."""
        ...
