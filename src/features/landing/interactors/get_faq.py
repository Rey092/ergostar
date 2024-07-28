"""GetFaqInteractor interactor."""
from src.features.landing.entities import (
    LandingSettings
)
from . import interfaces


class GetFaqInteractor:
    """Get home page interactor."""

    def __init__(
        self,
        landing_settings_repository: interfaces.IGetOneLandingSettings,
    ):
        """Initialize the interactor."""
        self._landing_settings_repository = landing_settings_repository

    async def __call__(self) -> dict:
        """Execute the interactor."""
        landing_settings: LandingSettings = await self._landing_settings_repository.get_one()

        return {
            "landing_settings": landing_settings,
        }
