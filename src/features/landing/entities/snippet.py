from dataclasses import dataclass, field
from datetime import datetime
from src.common.base.entity import Entity


@dataclass
class LandingSnippet(Entity):
    """Landing snippet entity."""

    tab: str
    title: str
    subtitle: str
    description: str
    code: str
    code_language: str
    feather_icon: str
    id: int = field(init=True, default=None)
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
