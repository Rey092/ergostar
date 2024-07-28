"""Interfaces for Landing Home Page Repositories."""

from abc import abstractmethod
from typing import Protocol

from src.features.landing.entities import (
    LandingSettings
)


class ISeedLandingSettings(Protocol):
    """IGetOneLandingSettings"""

    @abstractmethod
    async def add(self, obj: LandingSettings) -> LandingSettings:
        """Add landing settings."""
        ...

    @abstractmethod
    async def exists(self) -> bool:
        """Check if landing settings exist."""
        ...
