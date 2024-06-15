from typing import Any

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from db.models import LandingSettings
from src.landing.repositories.landing_settings import LandingSettingsRepository


class LandingSettingsService(SQLAlchemyAsyncRepositoryService[LandingSettings]):
    """LandingSettings Service."""

    repository_type = LandingSettingsRepository
    match_fields = ["name"]

    def __init__(self, **repo_kwargs: Any) -> None:
        """Initialize the service."""
        self.repository: LandingSettingsRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type
        super().__init__(**repo_kwargs)
