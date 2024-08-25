"""Base entity classes."""

import uuid
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapper
    from sqlalchemy.sql import FromClause


@dataclass(kw_only=True)
class Entity:
    """Base entity class."""

    if TYPE_CHECKING:
        __table__: FromClause = field(init=False)
        __mapper__: Mapper[Any] = field(init=False)
        __name__: str = field(init=False)

    # noinspection PyArgumentList
    @classmethod
    def from_dict(cls, data: dict) -> "Entity":
        """Create entity from dictionary."""
        # Get the set of field names in the dataclass
        field_names = {f.name for f in fields(cls)}

        # Filter the dictionary to only include keys that are dataclass fields
        filtered_data = {k: v for k, v in data.items() if k in field_names}

        # Create and return an instance of the dataclass
        return cls(**filtered_data)

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        """Convert entity to dictionary."""
        if exclude is None:
            exclude = set()
        return asdict(
            self,
            dict_factory=lambda _: {k: v for k, v in _ if k not in exclude},
        )


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

    id: int | None = None


@dataclass(kw_only=True, eq=False)
class UUIDEntity(IdEntity, Entity):
    """UUID entity class."""

    id: uuid.UUID | None = None

    def __post_init__(self):
        """Convert 'id' to UUID if it is a string."""
        if isinstance(self.id, str):
            self.id = uuid.UUID(self.id)


@dataclass(kw_only=True, eq=False)
class BigIntAuditEntity(AuditEntity, BigIntEntity, Entity):
    """Big integer audit entity class."""


@dataclass(kw_only=True, eq=False)
class UUIDAuditEntity(AuditEntity, UUIDEntity, Entity):
    """UUID audit entity class."""
