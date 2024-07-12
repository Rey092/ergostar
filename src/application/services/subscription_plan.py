"""Landing Home Page Service."""

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.domain.entities.subscriptions import SubscriptionPlan
from src.infra.repositories.subscriptions.plan import SubscriptionPlanRepository


class SubscriptionPlanService(SQLAlchemyAsyncRepositoryService[SubscriptionPlan]):
    """HomePage Service."""

    repository: SubscriptionPlanRepository
    repository_type = SubscriptionPlanRepository

    async def list_available(self) -> list[SubscriptionPlan]:
        """List available plans."""
        return await self.repository.list_available()
