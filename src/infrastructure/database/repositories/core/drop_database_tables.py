"""Drop database tables repository module."""

from sqlalchemy import text

from src.application.interfaces.repositories.database import (
    IDropDatabaseTablesRepository,
)
from src.infrastructure.database.base import BaseAlchemyRepository


class DropDatabaseTablesRepository(
    BaseAlchemyRepository,
    IDropDatabaseTablesRepository,
):
    """Drop database repository."""

    async def drop_database_tables(self) -> None:
        """Drop database tables."""
        # drop and create the public schema, this will drop all tables
        drop_command = text("DROP SCHEMA IF EXISTS public CASCADE;")
        await self._session.execute(drop_command)

        # recreate the public schema, so we can migrate the database from scratch
        create_command = text("CREATE SCHEMA public;")
        await self._session.execute(create_command)
