"""Landing Solution Repository."""

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import true

from src.common.base.alchemy import AlchemyRepository
from src.features.landing.entities import LandingSolution
from src.features.landing.interactors.interfaces import IGetCarouserLandingSolutions


class LandingSolutionRepository(
    AlchemyRepository[LandingSolution],
    IGetCarouserLandingSolutions
):
    """Team Repository."""

    model_type = LandingSolution

    async def list_active_solutions_for_carousel(self) -> list[LandingSolution]:
        """Get carousel string."""
        landing_solutions_carousel: list[LandingSolution] = await self._repository.list(
            statement=select(LandingSolution)
            .where(LandingSolution.is_carousel_active == true())
            .order_by(func.random()),
        )

        return landing_solutions_carousel

    async def list_top_banners(self) -> list[LandingSolution]:
        """List top banners."""
        return await self._repository.list(
            statement=select(LandingSolution)
            .where(LandingSolution.is_top_active == true())
            .order_by(func.random())
            .limit(3)
        )
