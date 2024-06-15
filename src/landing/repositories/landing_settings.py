from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository

from db.models import LandingSettings


class LandingSettingsRepository(SQLAlchemyAsyncSlugRepository[LandingSettings]):
    """Team Repository."""

    model_type = LandingSettings
