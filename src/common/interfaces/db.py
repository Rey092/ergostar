"""Common interfaces."""
from typing import Protocol, TypeVar, Any, Optional, Iterable
from sqlalchemy import Result, TextClause, Executable
from sqlalchemy.sql.selectable import TypedReturnsRows, ForUpdateParameter
# noinspection PyProtectedMember
from sqlalchemy.engine.interfaces import _CoreAnyExecuteParams  # noqa: F401

_T = TypeVar("_T", bound=Any)


class IDatabaseSession(Protocol):
    """IAlchemySession protocol."""

    async def commit(self) -> None:
        """Commit the transaction."""
        ...

    async def flush(self) -> None:
        """Flush the session."""
        ...

    async def execute(
        self,
        statement: Executable,
        params: Optional[_CoreAnyExecuteParams] = None,
    ) -> Result[_T]:
        ...

    async def refresh(
        self,
        instance: object,
        attribute_names: Optional[Iterable[str]] = None,
        with_for_update: ForUpdateParameter = None,
    ) -> None:
        """Refresh the given instance with the most recent state from the database."""
        ...
