"""Interfaces for Landing Home Page Repositories."""

from abc import abstractmethod
from collections.abc import Sequence

from advanced_alchemy.repository import SQLAlchemyAsyncRepositoryProtocol

from src.domain.entities.landing import LandingSnippet
from src.domain.entities.landing import LandingSolution
from src.domain.entities.landing.home_page import LandingHomePage
from src.domain.entities.landing.settings import LandingSettings


class LandingHomePageRepositoryInterface(
    SQLAlchemyAsyncRepositoryProtocol[LandingHomePage]
):
    """LandingHomePage Repository."""

    model_type = LandingHomePage


class LandingSettingsRepositoryInterface(
    SQLAlchemyAsyncRepositoryProtocol[LandingHomePage]
):
    """LandingSettings Repository."""

    model_type = LandingSettings


class LandingSnippetRepositoryInterface(
    SQLAlchemyAsyncRepositoryProtocol[LandingHomePage]
):
    """LandingSnippet Repository."""

    model_type = LandingSnippet

    @abstractmethod
    async def list_active(self) -> Sequence[LandingSnippet]:
        """List active snippets."""


class LandingSolutionRepositoryInterface(
    SQLAlchemyAsyncRepositoryProtocol[LandingHomePage]
):
    """LandingSolution Repository."""

    model_type = LandingSolution

    @abstractmethod
    async def list_active_solutions_for_carousel(self) -> Sequence[LandingSolution]:
        """Get LandingSolutions for carousel string."""

    @abstractmethod
    async def list_top_banners(self) -> Sequence[LandingSolution]:
        """List top banners."""
