"""ValueObject base."""

from abc import ABC
from dataclasses import dataclass
from typing import Any
from typing import Generic
from typing import TypeVar

V = TypeVar("V", bound=Any)


@dataclass(frozen=True)
class BaseValueObject:
    """Base value object."""

    def __post_init__(self) -> None:
        """Validate value object."""
        self._validate()

    def _validate(self) -> None:
        """Validate value object."""


@dataclass(frozen=True)
class ValueObject(BaseValueObject, ABC, Generic[V]):
    """ValueObject base class."""

    value: V

    def to_raw(self) -> V:
        """Return raw value."""
        return self.value

    def __eq__(self, other: object) -> bool:
        """Check if value objects are equal."""
        if not isinstance(other, self.__class__):
            return self.value == other
        return self.value == other.value
