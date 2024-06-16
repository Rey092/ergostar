from typing import Any

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from db.models import LandingHomePage
from src.landing.repositories.landing_home_page import LandingHomePageRepository


class LandingHomePageService(SQLAlchemyAsyncRepositoryService[LandingHomePage]):
    """HomePage Service."""

    repository_type = LandingHomePageRepository
    match_fields = ["name"]

    def __init__(self, **repo_kwargs: Any) -> None:
        """Initialize the service."""
        self.repository: LandingHomePageRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type
        super().__init__(**repo_kwargs)
