"""Drop database tables interactor module."""

from sqlalchemy import text

from src.common.base.interactor import Interactor
from src.common.interfaces.database_session import IAlchemySession
from src.config.settings import AppSettings


class DropDatabaseTablesInteractor(Interactor[None, None]):
    """Drop database tables interactor."""

    def __init__(
        self,
        session: IAlchemySession,
        app_settings: AppSettings,
    ):
        """Initialize interactor."""
        self._session = session
        self._debug: bool = app_settings.DEBUG
        self._message_can_not_drop = "Cannot drop database in production."

    async def __call__(
        self,
        request_model: None = None,
        **kwargs,
    ) -> None:
        """Drop database tables."""
        # check if we are in production
        if not self._debug:
            raise ValueError(self._message_can_not_drop)

        # drop and create the public schema, this will drop all tables
        drop_command = text("DROP SCHEMA IF EXISTS public CASCADE;")
        await self._session.execute(drop_command)

        # recreate the public schema, so we can migrate the database from scratch
        create_command = text("CREATE SCHEMA public;")
        await self._session.execute(create_command)

        # commit the transaction
        await self._session.commit()
