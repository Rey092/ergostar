"""Landing settings service."""

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from db.models import LandingSnippet
from src.landing.repositories.landing_snippet import LandingSnippetRepository


class LandingSnippetService(SQLAlchemyAsyncRepositoryService[LandingSnippet]):
    """LandingSnippet Service."""

    repository: LandingSnippetRepository
    repository_type = LandingSnippetRepository

    async def list_active(self) -> list[LandingSnippet]:
        """List active snippets."""
        return await self.repository.list_active()
