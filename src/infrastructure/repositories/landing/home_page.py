"""Landing home page repository."""

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.domain.entities.landing.home_page import LandingHomePage
from src.application.services.interfaces.repositories import (
    LandingHomePageRepositoryInterface,
)


class LandingHomePageRepository(
    SQLAlchemyAsyncRepository[LandingHomePage],
    LandingHomePageRepositoryInterface
):
    """LandingHomePageRepository."""

    model_type = LandingHomePage
