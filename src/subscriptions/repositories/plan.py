"""SubscriptionPlan repository."""

from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository
from sqlalchemy import select
from sqlalchemy import true

from src.subscriptions.domain import SubscriptionPlan


class SubscriptionPlanRepository(SQLAlchemyAsyncSlugRepository[SubscriptionPlan]):
    """Team Repository."""

    model_type = SubscriptionPlan

    async def list_available(self) -> list[SubscriptionPlan]:
        """List available plans."""
        return await self.list(
            statement=select(SubscriptionPlan).where(
                SubscriptionPlan.is_public == true()
            )
        )
