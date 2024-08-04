"""API key entity."""

from dataclasses import dataclass
from dataclasses import field

from uuid_utils import uuid7

from src.common.base.entity import BigIntAuditEntity


@dataclass(eq=False)
class ApiKey(BigIntAuditEntity):
    """API key entity."""

    user_id: int
    key: str = field(default_factory=uuid7)
