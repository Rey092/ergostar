"""Repository for subscription plan feature."""

from collections.abc import Sequence

from src.application.interfaces.repositories.seed import ISeedRepository
from src.domain.entities.subscriptions import SubscriptionPlan
from src.infrastructure.database.base import AlchemyRepository
from src.infrastructure.database.base import GenericAlchemyRepository


# noinspection DuplicatedCode
class SubscriptionPlanRepository(
    AlchemyRepository[SubscriptionPlan],
    ISeedRepository[SubscriptionPlan],
):
    """Subscription Plan repository."""

    entity_type = SubscriptionPlan
    repository_type = GenericAlchemyRepository[SubscriptionPlan]

    async def add_many(
        self,
        data: list[SubscriptionPlan],
    ) -> Sequence[SubscriptionPlan]:
        """Add many entries."""
        return await self._repository.add_many(data)

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._repository.delete_where()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._repository.exists()
