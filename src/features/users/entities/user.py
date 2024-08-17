"""User entities."""

from dataclasses import dataclass

from advanced_alchemy.base import ModelProtocol

from src.common.base.entity import UUIDAuditEntity


@dataclass(eq=False)
class User(UUIDAuditEntity, ModelProtocol):
    """User entity."""

    email: str
