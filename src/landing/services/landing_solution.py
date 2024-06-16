"""Landing solution Service."""

from collections.abc import Sequence
from typing import Any

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import true

from db.models import LandingSolution
from src.landing.repositories.landing_solution import LandingSolutionRepository


class LandingSolutionService(SQLAlchemyAsyncRepositoryService[LandingSolution]):
    """LandingSolution Service."""

    repository_type = LandingSolutionRepository
    match_fields = ["name"]

    def __init__(self, **repo_kwargs: Any) -> None:
        """Initialize the service."""
        self.repository: LandingSolutionRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type
        super().__init__(**repo_kwargs)

    async def get_carousel_string(self) -> str:
        """Get carousel string."""
        landing_solutions_carousel: Sequence[LandingSolution] = await self.list(
            statement=select(LandingSolution)
            .where(LandingSolution.is_carousel_active == true())
            .order_by(func.random())
        )
        carousel_string: str = ", ".join(
            [f'"{service.title_carousel}"' for service in landing_solutions_carousel]
        )
        return carousel_string

    async def list_top_banners(self) -> Sequence[LandingSolution]:
        """List top banners."""
        return await self.list(
            statement=select(LandingSolution)
            .where(LandingSolution.is_top_active == true())
            .order_by(func.random())
            .limit(3)
        )
