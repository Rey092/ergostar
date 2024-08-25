"""API key entity."""

from dataclasses import dataclass
from uuid import UUID

from src.common.base.entity import UUIDAuditEntity


@dataclass(eq=False)
class ApiKeyEntity(UUIDAuditEntity):
    """API key entity."""

    user_id: UUID
    key_hashed: str
    key_original: UUID | None = None

    def __post_init__(self):
        """Convert 'user_id' to UUID if it is a string."""
        if isinstance(self.id, str):
            self.user_id = UUID(self.id)
