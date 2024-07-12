"""Interfaces for Landing Home Page Service."""

from abc import abstractmethod
from collections.abc import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.landing.domain import LandingSnippet, LandingSolution
from src.landing.domain.home_page import LandingHomePage
from src.landing.domain.settings import LandingSettings
from src.landing.services.interfaces.repositories import (
    LandingHomePageRepositoryInterface,
)
from src.landing.services.interfaces.repositories import (
    LandingSettingsRepositoryInterface,
)
from src.landing.services.interfaces.repositories import (
    LandingSnippetRepositoryInterface,
)
from src.landing.services.interfaces.repositories import (
    LandingSolutionRepositoryInterface,
)


class LandingHomePageRepositoryServiceInterface(
    SQLAlchemyAsyncRepositoryService[LandingHomePage]
):
    """LandingHomePage RepositoryService."""

    repository: LandingHomePageRepositoryInterface


class LandingSettingsRepositoryServiceInterface(
    SQLAlchemyAsyncRepositoryService[LandingSettings]
):
    """LandingSettings RepositoryService."""

    repository: LandingSettingsRepositoryInterface


class LandingSnippetRepositoryServiceInterface(
    SQLAlchemyAsyncRepositoryService[LandingSnippet]
):
    """LandingSnippet RepositoryService."""

    repository: LandingSnippetRepositoryInterface

    @abstractmethod
    async def list_active(self) -> Sequence[LandingSnippet]:
        """List active snippets."""
        raise NotImplementedError


class LandingSolutionRepositoryServiceInterface(
    SQLAlchemyAsyncRepositoryService[LandingSolution]
):
    """LandingSolution RepositoryService."""

    repository: LandingSolutionRepositoryInterface

    @abstractmethod
    async def get_carousel_string(self) -> str:
        """Get carousel string."""
        raise NotImplementedError

    @abstractmethod
    async def list_top_banners(self) -> Sequence[LandingSolution]:
        """List top banners."""
        raise NotImplementedError
