from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository

from db.models import LandingHomePage


class LandingHomePageRepository(SQLAlchemyAsyncSlugRepository[LandingHomePage]):
    """Team Repository."""

    model_type = LandingHomePage
