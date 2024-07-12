"""Landing settings repository."""

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from src.landing.domain.settings import LandingSettings
from src.landing.services.interfaces.repositories import (
    LandingSettingsRepositoryInterface,
)


class LandingSettingsRepository(
    SQLAlchemyAsyncRepository[LandingSettings],
    LandingSettingsRepositoryInterface
):
    """LandingSettingsRepository."""

    model_type = LandingSettings
