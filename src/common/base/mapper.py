"""Entity-Model Mapper base."""

from typing import Any
from typing import Protocol
from typing import cast
from typing import get_args

from advanced_alchemy.repository import ModelT

from src.common.interfaces.mapper import IMapper
from src.common.types import EntityT


class DefaultMapper(
    IMapper[EntityT, ModelT],
    Protocol[EntityT, ModelT],
):
    """Default Mapper."""

    def entity_to_model(self, entity: EntityT) -> ModelT:
        """Convert entity to model."""
        model_cls = get_args(self.__class__.__orig_bases__[0])[1]  # type: ignore[attr-defined]
        data: dict = entity.to_dict()
        valid_fields = {
            k: v for k, v in data.items() if k in model_cls.__table__.columns
        }
        return model_cls(**valid_fields)

    def model_to_entity(self, model: ModelT) -> EntityT:
        """Convert model to entity."""
        entity_cls = get_args(self.__class__.__orig_bases__[0])[0]  # type: ignore[attr-defined]
        return cast(EntityT, entity_cls.from_dict(model.to_dict()))


class AdapterMapper(
    IMapper[EntityT, ModelT],
    Protocol[EntityT, ModelT],
):
    """Adapter Mapper."""

    _adaptee: Any

    def entity_to_model(self, entity: EntityT) -> ModelT:
        """Convert entity to model."""
        return self._adaptee.entity_to_model(entity)

    def model_to_entity(self, model: ModelT) -> EntityT:
        """Convert model to entity."""
        return self._adaptee.model_to_entity(model)
