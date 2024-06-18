"""Landing Home Page Service."""

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from db.models import LandingHomePage
from src.landing.repositories.landing_home_page import LandingHomePageRepository


class LandingHomePageService(SQLAlchemyAsyncRepositoryService[LandingHomePage]):
    """HomePage Service."""

    repository_type = LandingHomePageRepository
