"""Repository base class"""
from typing import Generic, Type

from advanced_alchemy.repository import (
    ModelT,
    SQLAlchemyAsyncSlugRepositoryProtocol,
    SQLAlchemyAsyncSlugRepository
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.interfaces.db import IDatabaseSession


class AlchemyRepository(Generic[ModelT]):
    """Repository base class"""

    model_type: Type[ModelT]
    repository_type = SQLAlchemyAsyncSlugRepository[ModelT]
    _repository: SQLAlchemyAsyncSlugRepositoryProtocol[ModelT]
    _session: IDatabaseSession

    def __init__(
        self,
        session: IDatabaseSession,
    ) -> None:
        """Configure the repository object."""
        self._session = session
        self._repository = self.repository_type(
            session=session,
            statement=select(self.model_type),
            auto_expunge=False,
            auto_refresh=False,
            auto_commit=False,
        )
        self._repository.model_type = self.model_type
