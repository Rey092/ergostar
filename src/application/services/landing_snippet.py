"""Landing settings service."""

from src.domain.entities.landing import LandingSnippet
from src.infra.repositories.landing.snippet import LandingSnippetRepository
from src.application.services.interfaces.services import (
    LandingSnippetRepositoryServiceInterface,
)


class LandingSnippetService(LandingSnippetRepositoryServiceInterface):
    """LandingSnippet Service."""

    repository: LandingSnippetRepository
    repository_type = LandingSnippetRepository

    async def list_active(self) -> list[LandingSnippet]:
        """List active snippets."""
        return await self.repository.list_active()
