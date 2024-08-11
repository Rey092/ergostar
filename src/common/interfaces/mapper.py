"""Mapper interface."""

from abc import abstractmethod
from typing import Protocol

from advanced_alchemy.repository import ModelT

from src.common.types import EntityT


class IMapper(Protocol[EntityT, ModelT]):
    """Mapper interface."""

    @abstractmethod
    def entity_to_model(self, entity: EntityT) -> ModelT:
        """Convert entity to model."""
        raise NotImplementedError

    @abstractmethod
    def model_to_entity(self, model: ModelT) -> EntityT:
        """Convert model to entity."""
        raise NotImplementedError
