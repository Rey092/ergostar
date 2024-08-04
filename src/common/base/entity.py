"""Base entity classes."""

import uuid
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import UTC
from datetime import datetime

from dacite import from_dict


@dataclass(kw_only=True)
class Entity:
    """Base entity class."""

    @classmethod
    def from_dict(cls, data: dict) -> "Entity":
        """Create entity from dictionary."""
        return from_dict(data_class=cls, data=data)

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return asdict(self)


@dataclass(kw_only=True, eq=False)
class IdEntity:
    """Entity class with an id field."""

    id: object | None = field(default=None)

    def __hash__(self) -> int:
        """Entity hash based on id."""
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        """Compare entity id."""
        if not isinstance(other, IdEntity):
            return NotImplemented
        return self.id == other.id


@dataclass(kw_only=True, eq=False)
class AuditEntity:
    """Entity class with audit fields."""

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(kw_only=True, eq=False)
class BigIntEntity(IdEntity, Entity):
    """Big integer entity class."""

    id: int | None = field(default=None)


@dataclass(kw_only=True, eq=False)
class UUIDEntity(IdEntity, Entity):
    """UUID entity class."""

    id: uuid.UUID | None = field(default=None)


@dataclass(kw_only=True, eq=False)
class BigIntAuditEntity(AuditEntity, BigIntEntity, Entity):
    """Big integer audit entity class."""


@dataclass(kw_only=True, eq=False)
class UUIDAuditEntity(AuditEntity, UUIDEntity, Entity):
    """UUID audit entity class."""
