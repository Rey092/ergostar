"""Repository base."""

from abc import abstractmethod
from typing import Generic
from typing import Protocol
from typing import TypeVar

from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository
from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepositoryProtocol
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.common.types import EntityT
from src.infrastructure.interfaces.repository import IRepository


class GenericAlchemyRepositoryProtocol(
    SQLAlchemyAsyncSlugRepositoryProtocol[EntityT],
):
    """Generic repository protocol for SQLAlchemy."""


class GenericAlchemyRepository(
    SQLAlchemyAsyncSlugRepository[EntityT],
    GenericAlchemyRepositoryProtocol[EntityT],
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


class ModelEntityProtocol(Protocol[EntityT]):
    """Model-Entity protocol."""

    entity_type: type[EntityT]


class IGenericRepositoryProtocol(Protocol[EntityT]):
    """Protocol for repositories with a generic repository attribute."""

    @property
    @abstractmethod
    def generic_repository(self) -> GenericAlchemyRepositoryProtocol[EntityT]:
        """Return the generic repository."""
        ...


AlchemyRepositoryContractT = TypeVar(
    "AlchemyRepositoryContractT",
    bound=IGenericRepositoryProtocol,
)


class AlchemyRepository(
    BaseAlchemyRepository,
    ModelEntityProtocol[EntityT],
    IGenericRepositoryProtocol[EntityT],
    Generic[EntityT],
):
    """Base repository class with generic repository support."""

    repository_type = GenericAlchemyRepository
    _repository: GenericAlchemyRepositoryProtocol[EntityT]

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Configure the repository object."""
        super().__init__(session=session)
        self._repository = self.repository_type(
            session=self._session,
            statement=select(self.entity_type),
            auto_expunge=False,
            auto_refresh=False,
            auto_commit=False,
        )
        self._repository.model_type = self.entity_type

    @property
    def generic_repository(self) -> GenericAlchemyRepositoryProtocol[EntityT]:
        """Return the generic repository."""
        return self._repository
