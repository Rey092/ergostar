"""API key entity."""

from dataclasses import dataclass
from dataclasses import field

from src.common.base.entity import BigIntAuditEntity
from src.config.utils.uuid import generate_uuid7


@dataclass(eq=False)
class ApiKey(BigIntAuditEntity):
    """API key entity."""

    user_id: int
    key: str = field(default_factory=generate_uuid7)
