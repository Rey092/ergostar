"""API key entity."""

import uuid
from dataclasses import dataclass

from src.common.base.entity import UUIDAuditEntity


@dataclass(eq=False)
class ApiKey(UUIDAuditEntity):
    """API key entity."""

    user_id: uuid.UUID
    key_hashed: str
    key_original: uuid.UUID | None = None
