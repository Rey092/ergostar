"""Module init for landing repositories."""
from .home_page import LandingHomePageRepository
from .settings import LandingSettingsRepository
from .snippet import LandingSnippetRepository
from .solution import LandingSolutionRepository

__all__ = [
    "LandingHomePageRepository",
    "LandingSettingsRepository",
    "LandingSnippetRepository",
    "LandingSolutionRepository",
]
