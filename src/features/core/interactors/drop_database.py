"""Drop database interactor module."""
from sqlalchemy import text
from src.common.interfaces.db import IDatabaseSession
from src.common.types import SETTINGS_DEBUG
from src.config.settings import AppSettings


class DropDatabaseInteractor:
    """Drop database interactor."""

    def __init__(
        self,
        session: IDatabaseSession,
        debug: SETTINGS_DEBUG,
    ):
        """Initialize interactor."""
        self._session = session
        self._debug = debug

    async def __call__(self):
        """Drop database."""
        # check if we are in production
        if not self._debug:
            raise ValueError("Cannot drop database in production.")

        # drop and create the public schema, this will drop all tables
        drop_command = text("DROP SCHEMA IF EXISTS public CASCADE;")
        create_command = text("CREATE SCHEMA public;")
        await self._session.execute(drop_command)
        await self._session.execute(create_command)
        await self._session.commit()
