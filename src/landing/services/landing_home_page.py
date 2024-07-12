"""Landing Home Page Service."""

from src.landing.repositories import LandingHomePageRepository
from src.landing.services.interfaces.services import (
    LandingHomePageRepositoryServiceInterface,
)


class LandingHomePageService(LandingHomePageRepositoryServiceInterface):
    """HomePage Service."""

    repository: LandingHomePageRepository
    repository_type = LandingHomePageRepository
