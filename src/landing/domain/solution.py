from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class LandingSolution:
    """LandingSolution entity."""

    title: str
    title_carousel: str
    description: str
    docs_url: str = "https://google.com"
    is_top_active: bool = True
    is_carousel_active: bool = True
    id: int = field(init=False, default=None)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
