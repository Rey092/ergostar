"""Domain module for landing page."""
from .home_page import LandingHomePage
from .settings import LandingSettings
from .snippet import LandingSnippet
from .solution import LandingSolution
from src.features.landing.enums import LandingSnippetLanguage

__all__ = [
    # Entities
    "LandingSettings",
    "LandingHomePage",
    "LandingSnippet",
    "LandingSolution",
    # Enums
    "LandingSnippetLanguage"
]
