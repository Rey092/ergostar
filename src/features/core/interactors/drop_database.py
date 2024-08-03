"""Drop database interactor module."""

from sqlalchemy import text

from src.common.interfaces.db import IDatabaseSession
from src.config.settings import AppSettings


class DropDatabaseInteractor:
    """Drop database interactor."""

    def __init__(
        self,
        session: IDatabaseSession,
        app_settings: AppSettings,
    ):
        """Initialize interactor."""
        self._session = session
        self._debug: bool = app_settings.DEBUG
        self._message_can_not_drop = "Cannot drop database in production."

    async def __call__(self):
        """Drop database."""
        # check if we are in production
        if not self._debug:
            raise ValueError(self._message_can_not_drop)

        # drop and create the public schema, this will drop all tables
        drop_command = text("DROP SCHEMA IF EXISTS public CASCADE;")
        create_command = text("CREATE SCHEMA public;")
        await self._session.execute(drop_command)
        await self._session.execute(create_command)
        await self._session.commit()
