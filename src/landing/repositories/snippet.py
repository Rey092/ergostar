"""Landing Snippet Repository."""

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import select
from sqlalchemy import true

from src.landing.domain import LandingSnippet
from src.landing.services.interfaces.repositories import (
    LandingSnippetRepositoryInterface,
)


class LandingSnippetRepository(
    SQLAlchemyAsyncRepository[LandingSnippet], LandingSnippetRepositoryInterface
):
    """Team Repository."""

    model_type = LandingSnippet

    async def list_active(self) -> list[LandingSnippet]:
        """List active snippets."""
        return await self.list(
            statement=select(LandingSnippet).where(LandingSnippet.is_active == true())
        )
