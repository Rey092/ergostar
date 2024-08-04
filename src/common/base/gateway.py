"""Gateway base."""

from typing import Generic
from typing import cast

from advanced_alchemy.repository import ModelT
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.base.repository import GenericSQLAlchemyRepository
from src.common.base.repository import GenericSQLAlchemyRepositoryProtocol
from src.common.interfaces.db import IDatabaseSession


class AlchemyGateway(Generic[ModelT]):
    """Gateway base class."""

    model_type: type[ModelT]
    repository_type = GenericSQLAlchemyRepository
    _repository: GenericSQLAlchemyRepositoryProtocol[ModelT]
    _session: IDatabaseSession

    def __init__(
        self,
        session: IDatabaseSession,
    ) -> None:
        """Configure the repository object."""
        self._session: AsyncSession = cast(AsyncSession, session)
        self._repository = self.repository_type(
            session=self._session,
            statement=select(self.model_type),
            auto_expunge=False,
            auto_refresh=False,
            auto_commit=False,
        )
        self._repository.model_type = self.model_type
