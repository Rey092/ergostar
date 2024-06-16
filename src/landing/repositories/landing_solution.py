from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository

from db.models import LandingSolution


class LandingSolutionRepository(SQLAlchemyAsyncSlugRepository[LandingSolution]):
    """Team Repository."""

    model_type = LandingSolution
