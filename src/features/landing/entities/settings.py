"""Domain entity for landing home page."""
from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.common.base.entity import Entity


@dataclass
class LandingSettings(Entity):
    """Home page model."""

    id: int = field(init=False, default=None)
    title: str = "Title"
    footer_description: str = "Footer description"
    footer_rights: str = "Footer rights"
    url_login: str = "https://login.example.com"
    url_api_docs: str = "https://docs.example.com"
    url_register: str = "https://register.example.com"
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=None))
    updated_at: datetime = field(default_factory=lambda: datetime.now(tz=None))
