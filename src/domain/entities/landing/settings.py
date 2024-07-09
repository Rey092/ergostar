"""Domain entity for landing home page."""
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class LandingSettings:
    """Home page model."""

    id: int = field(init=False, default=None)
    title: str = "Title"
    footer_description: str = "Footer description"
    footer_rights: str = "Footer rights"
    url_login: str = "https://login.example.com"
    url_api_docs: str = "https://docs.example.com"
    url_register: str = "https://register.example.com"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
