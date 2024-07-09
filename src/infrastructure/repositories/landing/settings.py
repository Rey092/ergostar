"""Landing settings repository."""

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from src.domain.entities.landing.settings import LandingSettings
from src.application.services.interfaces.repositories import (
    LandingSettingsRepositoryInterface,
)


class LandingSettingsRepository(
    SQLAlchemyAsyncRepository[LandingSettings],
    LandingSettingsRepositoryInterface
):
    """LandingSettingsRepository."""

    model_type = LandingSettings
