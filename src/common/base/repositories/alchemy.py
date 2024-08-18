"""Repository base."""

from abc import ABC
from typing import Generic
from typing import Protocol
from typing import TypeVar

from advanced_alchemy.repository import ModelT
from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository
from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepositoryProtocol
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.base.mapper import AdapterMapper
from src.common.base.mapper import DefaultMapper
from src.common.interfaces.mapper import IMapper
from src.common.interfaces.repository import IRepository
from src.common.types import EntityT


class GenericAlchemyRepositoryProtocol(
    SQLAlchemyAsyncSlugRepositoryProtocol[ModelT],
):
    """Generic repository protocol for SQLAlchemy."""


class GenericAlchemyRepository(
    SQLAlchemyAsyncSlugRepository[ModelT],
    GenericAlchemyRepositoryProtocol[ModelT],
):
    """Generic repository for SQLAlchemy."""


class BaseAlchemyRepository(IRepository):
    """Base repository class."""

    _session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Configure the repository object."""
        self._session: AsyncSession = session


class ModelEntityProtocol(Protocol[ModelT, EntityT]):
    """Model-Entity protocol."""

    model_type: type[ModelT]
    entity_type: type[EntityT]


class AbstractAlchemyRepository(
    BaseAlchemyRepository,
    ModelEntityProtocol,
    IMapper,
    ABC,
    Generic[EntityT, ModelT],
):
    """Base repository class with generic repository support."""

    repository_type = GenericAlchemyRepository
    _repository: GenericAlchemyRepositoryProtocol[ModelT]

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
    def generic_repository(self) -> GenericAlchemyRepositoryProtocol[ModelT]:
        """Return the generic repository."""
        return self._repository


class AlchemyRepository(
    DefaultMapper[EntityT, ModelT],
    AbstractAlchemyRepository[EntityT, ModelT],
):
    """AlchemyMappedRepository."""


MappedRepoT = TypeVar("MappedRepoT", bound=AlchemyRepository)


class AlchemyAdapterRepository(
    BaseAlchemyRepository,
    ModelEntityProtocol[ModelT, EntityT],
    AdapterMapper[EntityT, ModelT],
    Generic[EntityT, ModelT, MappedRepoT],
):
    """AlchemyAdapterRepository."""

    _adaptee: MappedRepoT
    _repository: GenericAlchemyRepositoryProtocol[ModelT]

    def __init__(
        self,
        session: AsyncSession,
        mapped_repo: MappedRepoT,
    ) -> None:
        """Configure the repository object."""
        super().__init__(session=session)
        self._adaptee = mapped_repo
        self._repository = self._adaptee.generic_repository
