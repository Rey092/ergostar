"""Mock services for landing module."""

from collections.abc import Sequence

from src.application.services.interfaces.services import LandingHomePageRepositoryServiceInterface, \
    LandingSettingsRepositoryServiceInterface, LandingSnippetRepositoryServiceInterface, \
    LandingSolutionRepositoryServiceInterface
from src.domain.entities.landing import LandingSnippet
from src.domain.entities.landing import LandingSolution


class MockLandingHomePageService(LandingHomePageRepositoryServiceInterface):
    """LandingHomePage RepositoryService."""


class MockLandingSettingsService(LandingSettingsRepositoryServiceInterface):
    """LandingSettings RepositoryService."""


class MockLandingSnippetService(LandingSnippetRepositoryServiceInterface):
    """LandingSnippet RepositoryService."""

    async def list_active(self) -> Sequence[LandingSnippet]:
        """List active snippets."""
        raise NotImplementedError


class MockLandingSolutionService(LandingSolutionRepositoryServiceInterface):
    """LandingSolution RepositoryService."""

    async def get_carousel_string(self) -> Sequence[LandingSolution]:
        """Get carousel string."""
        raise NotImplementedError

    async def list_top_banners(self) -> Sequence[LandingSolution]:
        """List top banners."""
        raise NotImplementedError
