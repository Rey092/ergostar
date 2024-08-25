"""User entities."""

from dataclasses import dataclass

from src.common.base.entity import UUIDAuditEntity


@dataclass(eq=False)
class UserEntity(UUIDAuditEntity):
    """User entity."""

    email: str
