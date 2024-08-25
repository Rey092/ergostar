"""Repository for subscription plan feature."""

from collections.abc import Sequence

from src.common.base.repositories.alchemy import AlchemyRepository
from src.common.base.repositories.alchemy import GenericAlchemyRepository
from src.features.subscriptions.public.entities import SubscriptionPlanEntity
from src.features.subscriptions.public.interfaces import (
    ISubscriptionPlanRepositoryContract,
)


# noinspection DuplicatedCode
class SubscriptionPlanRepository(
    AlchemyRepository[SubscriptionPlanEntity],
    ISubscriptionPlanRepositoryContract[SubscriptionPlanEntity],
):
    """Subscription Plan repository."""

    entity_type = SubscriptionPlanEntity
    repository_type = GenericAlchemyRepository[SubscriptionPlanEntity]

    async def add_many(
        self,
        data: list[SubscriptionPlanEntity],
    ) -> Sequence[SubscriptionPlanEntity]:
        """Add many entries."""
        return await self._repository.add_many(data)

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._repository.delete_where()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._repository.exists()
