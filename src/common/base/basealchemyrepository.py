"""Repository base."""

from abc import ABC
from typing import Generic
from typing import TypeVar
from typing import cast

from advanced_alchemy.repository import ModelT
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.base.mapper import AdapterMapper
from src.common.base.mapper import DefaultMapper
from src.common.base.repository_generic import GenericSQLAlchemyRepository
from src.common.base.repository_generic import GenericSQLAlchemyRepositoryProtocol
from src.common.interfaces.database_session import IAlchemySession
from src.common.interfaces.mapper import IMapper
from src.common.types import EntityT


class BaseAlchemyRepository(Generic[EntityT, ModelT]):
    """Base repository class."""

    model_type: type[ModelT]
    entity_type: type[EntityT]
    _session: IAlchemySession

    def __init__(
        self,
        session: IAlchemySession,
    ) -> None:
        """Configure the repository object."""
        self._session: AsyncSession = cast(AsyncSession, session)


class AlchemyRepository(BaseAlchemyRepository, IMapper, ABC, Generic[EntityT, ModelT]):
    """Base repository class with generic repository support."""

    repository_type = GenericSQLAlchemyRepository
    _repository: GenericSQLAlchemyRepositoryProtocol[ModelT]

    def __init__(
        self,
        session: IAlchemySession,
    ) -> None:
        """Configure the repository object."""
        super().__init__(session=session)
        self._repository = self.repository_type(
            session=cast(AsyncSession, self._session),
            statement=select(self.model_type),
            auto_expunge=False,
            auto_refresh=False,
            auto_commit=False,
        )
        self._repository.model_type = self.model_type


class AlchemyMappedRepository(
    DefaultMapper[EntityT, ModelT],
    AlchemyRepository[EntityT, ModelT],
    Generic[EntityT, ModelT],
):
    """AlchemyMappedRepository."""


MappedRepoT = TypeVar("MappedRepoT", bound=AlchemyMappedRepository)


class AlchemyAdapterRepository(
    AdapterMapper[EntityT, ModelT],
    AlchemyRepository[EntityT, ModelT],
    Generic[EntityT, ModelT, MappedRepoT],
):
    """AlchemyAdapterRepository."""

    _adaptee: MappedRepoT

    def __init__(
        self,
        session: IAlchemySession,
        mapped_repo: MappedRepoT,
    ) -> None:
        """Configure the repository object."""
        super().__init__(session=session)
        self._adaptee = mapped_repo
