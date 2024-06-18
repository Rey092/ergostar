"""Landing settings service."""

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from db.models import LandingSettings
from src.landing.repositories.landing_settings import LandingSettingsRepository


class LandingSettingsService(SQLAlchemyAsyncRepositoryService[LandingSettings]):
    """LandingSettings Service."""

    repository_type = LandingSettingsRepository
