"""Landing settings repository."""

from src.common.base.alchemy import AlchemyRepository
from src.features.landing.entities.settings import LandingSettings
from src.features.landing.interactors.interfaces import IGetOneLandingSettings
from src.features.landing.interactors.seed.interfaces import ISeedLandingSettings


class LandingSettingsRepository(
    AlchemyRepository[LandingSettings],
    IGetOneLandingSettings,
    ISeedLandingSettings,
):
    """LandingSettingsRepository."""

    model_type = LandingSettings

    async def get_one(self) -> LandingSettings:
        """Get one LandingSettings."""
        return await self._repository.get_one()

    async def exists(self) -> bool:
        """Check if landing settings exist."""
        return await self._repository.exists()

    async def add(self, obj: LandingSettings) -> LandingSettings:
        """Add landing settings."""
        return await self._repository.add(data=obj)
