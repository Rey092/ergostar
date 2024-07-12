"""Landing settings service."""

from src.landing.repositories import LandingSettingsRepository
from src.landing.services.interfaces.services import (
    LandingSettingsRepositoryServiceInterface,
)


class LandingSettingsService(LandingSettingsRepositoryServiceInterface):
    """LandingSettings Service."""

    repository_type = LandingSettingsRepository
