"""Landing settings service."""

from src.infra.repositories.landing.settings import LandingSettingsRepository
from src.application.services.interfaces.services import (
    LandingSettingsRepositoryServiceInterface,
)


class LandingSettingsService(LandingSettingsRepositoryServiceInterface):
    """LandingSettings Service."""

    repository_type = LandingSettingsRepository
