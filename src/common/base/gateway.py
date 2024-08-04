"""Gateway base."""

from typing import Generic
from typing import TypeVar
from typing import cast
from typing import get_args

from advanced_alchemy.repository import ModelT
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.base.entity import Entity
from src.common.base.repository import GenericSQLAlchemyRepository
from src.common.base.repository import GenericSQLAlchemyRepositoryProtocol
from src.common.interfaces.db import IDatabaseSession

EntityT = TypeVar("EntityT", bound=Entity)


class AlchemyGateway(Generic[EntityT, ModelT]):
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

    def entity_to_model(self, entity: EntityT) -> ModelT:
        """Convert entity to model."""
        model_cls = self._get_model_class()
        return model_cls(**entity.to_dict())

    def model_to_entity(self, model: ModelT) -> EntityT:
        """Convert model to entity."""
        entity_cls = self.get_entity_class()
        return cast(EntityT, entity_cls.from_dict(model.to_dict()))

    @classmethod
    def _get_model_class(cls) -> type[ModelT]:
        """Get the real class for ModelT."""
        return get_args(cls.__orig_bases__[0])[1]  # type: ignore[attr-defined]

    @classmethod
    def get_entity_class(cls) -> type[EntityT]:
        """Get the real class for EntityT."""
        return get_args(cls.__orig_bases__[0])[0]  # type: ignore[attr-defined]
