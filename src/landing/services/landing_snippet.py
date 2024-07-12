"""Landing settings service."""
from src.landing.domain import LandingSnippet
from src.landing.repositories import LandingSnippetRepository
from src.landing.services.interfaces.services import (
    LandingSnippetRepositoryServiceInterface,
)


class LandingSnippetService(LandingSnippetRepositoryServiceInterface):
    """LandingSnippet Service."""

    repository: LandingSnippetRepository
    repository_type = LandingSnippetRepository

    async def list_active(self) -> list[LandingSnippet]:
        """List active snippets."""
        return await self.repository.list_active()
