"""User entities."""

from dataclasses import dataclass

from src.common.base.entity import BigIntEntity


@dataclass(eq=False)
class User(BigIntEntity):
    """User entity."""

    email: str
