"""Landing home page repository."""

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.landing.domain.home_page import LandingHomePage
from src.landing.services.interfaces.repositories import (
    LandingHomePageRepositoryInterface,
)


class LandingHomePageRepository(
    SQLAlchemyAsyncRepository[LandingHomePage],
    LandingHomePageRepositoryInterface
):
    """LandingHomePageRepository."""

    model_type = LandingHomePage
