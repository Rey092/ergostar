"""Repository base."""

from abc import ABC
from typing import Generic
from typing import TypeVar

from advanced_alchemy.repository import ModelT
from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository
from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepositoryProtocol
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.base.mapper import AdapterMapper
from src.common.base.mapper import DefaultMapper
from src.common.interfaces.mapper import IMapper
from src.common.types import EntityT


class GenericSQLAlchemyRepositoryProtocol(
    SQLAlchemyAsyncSlugRepositoryProtocol[ModelT],
):
    """Generic repository protocol for SQLAlchemy."""


class GenericSQLAlchemyRepository(
    SQLAlchemyAsyncSlugRepository[ModelT],
    GenericSQLAlchemyRepositoryProtocol[ModelT],
):
    """Generic repository for SQLAlchemy."""


class BaseAlchemyRepository(Generic[EntityT, ModelT]):
    """Base repository class."""

    model_type: type[ModelT]
    entity_type: type[EntityT]
    _session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Configure the repository object."""
        self._session: AsyncSession = session


class AlchemyRepository(BaseAlchemyRepository, IMapper, ABC, Generic[EntityT, ModelT]):
    """Base repository class with generic repository support."""

    repository_type = GenericSQLAlchemyRepository
    _repository: GenericSQLAlchemyRepositoryProtocol[ModelT]

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Configure the repository object."""
        super().__init__(session=session)
        self._repository = self.repository_type(
            session=self._session,
            statement=select(self.model_type),
            auto_expunge=False,
            auto_refresh=False,
            auto_commit=False,
        )
        self._repository.model_type = self.model_type

    @property
    def repository(self) -> GenericSQLAlchemyRepositoryProtocol[ModelT]:
        """Return the repository object."""
        return self._repository


class AlchemyMappedRepository(
    DefaultMapper[EntityT, ModelT],
    AlchemyRepository[EntityT, ModelT],
):
    """AlchemyMappedRepository."""


MappedRepoT = TypeVar("MappedRepoT", bound=AlchemyMappedRepository)


class AlchemyAdapterRepository(
    BaseAlchemyRepository[EntityT, ModelT],
    AdapterMapper[EntityT, ModelT],
    Generic[EntityT, ModelT, MappedRepoT],
):
    """AlchemyAdapterRepository."""

    _adaptee: MappedRepoT
    _repository: GenericSQLAlchemyRepositoryProtocol[ModelT]

    def __init__(
        self,
        session: AsyncSession,
        mapped_repo: MappedRepoT,
    ) -> None:
        """Configure the repository object."""
        super().__init__(session=session)
        self._adaptee = mapped_repo
        self._repository = self._adaptee.repository
