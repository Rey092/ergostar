"""Landing Solution Repository."""

from collections.abc import Sequence

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import true

from src.domain.entities.landing import LandingSolution
from src.application.services.interfaces.repositories import (
    LandingSolutionRepositoryInterface,
)


class LandingSolutionRepository(
    SQLAlchemyAsyncRepository[LandingSolution], LandingSolutionRepositoryInterface
):
    """Team Repository."""

    model_type = LandingSolution

    async def list_active_solutions_for_carousel(self) -> Sequence[LandingSolution]:
        """Get carousel string."""
        landing_solutions_carousel: Sequence[LandingSolution] = await self.list(
            statement=select(LandingSolution)
            .where(LandingSolution.is_carousel_active == true())
            .order_by(func.random())
        )

        return landing_solutions_carousel

    async def list_top_banners(self) -> Sequence[LandingSolution]:
        """List top banners."""
        return await self.list(
            statement=select(LandingSolution)
            .where(LandingSolution.is_top_active == true())
            .order_by(func.random())
            .limit(3)
        )
