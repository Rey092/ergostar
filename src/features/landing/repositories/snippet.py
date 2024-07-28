"""Landing Snippet Repository."""
from src.common.base.alchemy import AlchemyRepository
from src.features.landing.entities import LandingSnippet
from src.features.landing.interactors.interfaces import IListActiveLandingSnippets


class LandingSnippetRepository(
    AlchemyRepository[LandingSnippet],
    IListActiveLandingSnippets
):
    """LandingSnippetRepository."""

    model_type = LandingSnippet

    async def list_active(self) -> list[LandingSnippet]:
        """List active snippets."""
        return await self._repository.list(is_active=True)
