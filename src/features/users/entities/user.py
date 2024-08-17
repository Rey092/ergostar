"""User entities."""

from dataclasses import dataclass

from src.common.base.entity import UUIDAuditEntity


@dataclass(eq=False)
class User(UUIDAuditEntity):
    """User entity."""

    email: str
