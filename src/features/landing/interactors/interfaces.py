"""Interfaces for Landing Home Page Repositories."""

from abc import abstractmethod
from typing import Protocol

from src.features.landing.entities import (
    LandingSnippet,
    LandingSolution,
    LandingHomePage,
    LandingSettings
)
from src.features.subscriptions import SubscriptionPlan


class IGetOneLandingHomePage(Protocol):
    """IGetOneLandingHomePage."""

    async def get_one(self) -> LandingHomePage:
        """Get one LandingHomePage."""
        ...


class IGetOneLandingSettings(Protocol):
    """IGetOneLandingSettings"""

    @abstractmethod
    async def get_one(self) -> LandingSettings:
        """Get one LandingSettings."""
        ...


class IListActiveLandingSnippets(Protocol):
    """IListActiveLandingSnippets."""

    @abstractmethod
    async def list_active(self) -> list[LandingSnippet]:
        """List active snippets."""
        ...


class IGetCarouserLandingSolutions(Protocol):
    """IGetCarouserLandingSolutions."""

    @abstractmethod
    async def list_active_solutions_for_carousel(self) -> list[LandingSolution]:
        """Get LandingSolutions for carousel string."""
        ...

    @abstractmethod
    async def list_top_banners(self) -> list[LandingSolution]:
        """List top banners."""
        ...


class IListPublicSubscriptionPlans(Protocol):
    """IListPublicSubscriptionPlans."""

    @abstractmethod
    async def list_public(self) -> list[SubscriptionPlan]:
        """List public subscription plans."""
        ...
