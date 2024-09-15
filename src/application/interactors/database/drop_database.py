"""Drop database tables interactor module."""

from litestar.exceptions import InternalServerException

from src.application.common.interactor import Interactor
from src.application.interfaces.repositories.database import (
    IDropDatabaseTablesRepository,
)
from src.infrastructure.common.interfaces import IDatabaseSession
from src.main.config.settings import AppSettings


class DropDatabaseInteractor(Interactor[None, None]):
    """Drop database tables interactor."""

    def __init__(
        self,
        session: IDatabaseSession,
        app_settings: AppSettings,
        drop_database_tables_repository: IDropDatabaseTablesRepository,
    ):
        """Initialize interactor."""
        self._session = session
        self._debug: bool = app_settings.DEBUG
        self._drop_database_tables_repository = drop_database_tables_repository
        self._message_can_not_drop = "Cannot drop database in production."

    async def __call__(
        self,
        request_model: None = None,
    ) -> None:
        """Drop database tables."""
        # check if we are in production
        if not self._debug:
            raise InternalServerException(self._message_can_not_drop)

        # drop and create the public schema
        await self._drop_database_tables_repository.drop_database_tables()

        # commit the transaction
        await self._session.commit()
