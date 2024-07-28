"""Landing home page repository."""
from src.common.base.alchemy import AlchemyRepository
from src.features.landing.entities import LandingHomePage
from src.features.landing.interactors.interfaces import IGetOneLandingHomePage


class LandingHomePageRepository(
    AlchemyRepository[LandingHomePage],
    IGetOneLandingHomePage
):
    """LandingHomePageRepository."""

    model_type = LandingHomePage

    async def get_one(self) -> LandingHomePage:
        """Get one LandingHomePage."""
        return await self._repository.get_one()
