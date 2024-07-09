"""Landing Home Page Service."""

from src.infrastructure.repositories.landing.home_page import LandingHomePageRepository
from src.application.services.interfaces.services import (
    LandingHomePageRepositoryServiceInterface,
)


class LandingHomePageService(LandingHomePageRepositoryServiceInterface):
    """HomePage Service."""

    repository: LandingHomePageRepository
    repository_type = LandingHomePageRepository
