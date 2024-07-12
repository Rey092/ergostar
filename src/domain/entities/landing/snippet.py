from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class LandingSnippet:
    """Landing snippet entity."""

    tab: str
    title: str
    subtitle: str
    description: str
    code: str
    code_language: str
    feather_icon: str
    is_active: bool = True
    id: int = field(init=False, default=None)
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
