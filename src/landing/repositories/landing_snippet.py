"""Landing Snippet Repository."""

from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository
from sqlalchemy import select
from sqlalchemy import true

from db.models import LandingSnippet


class LandingSnippetRepository(SQLAlchemyAsyncSlugRepository[LandingSnippet]):
    """Team Repository."""

    model_type = LandingSnippet

    async def list_active(self) -> list[LandingSnippet]:
        """List active snippets."""
        return await self.list(
            statement=select(LandingSnippet).where(LandingSnippet.is_active == true())
        )
