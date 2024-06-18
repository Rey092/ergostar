"""Landing solution Service."""

from collections.abc import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from db.models import LandingSolution
from src.landing.repositories.landing_solution import LandingSolutionRepository


class LandingSolutionService(SQLAlchemyAsyncRepositoryService[LandingSolution]):
    """LandingSolution Service."""

    repository: LandingSolutionRepository
    repository_type = LandingSolutionRepository

    async def get_carousel_string(self) -> str:
        """Get carousel string."""
        landing_solutions_carousel: Sequence[
            LandingSolution
        ] = await self.repository.list_active_solutions_for_carousel()
        carousel_string: str = ", ".join(
            [f'"{service.title_carousel}"' for service in landing_solutions_carousel]
        )
        return carousel_string

    async def list_top_banners(self) -> Sequence[LandingSolution]:
        """List top banners."""
        return await self.repository.list_top_banners()
