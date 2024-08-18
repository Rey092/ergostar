"""SubscriptionPlanRepositoryAdapter."""

from collections.abc import Sequence

from src.common.interfaces.fixture_loader.repository import ISeedManyEntries
from src.features.subscriptions.entities import SubscriptionPlanEntity
from src.features.subscriptions.repositories.subscription_plan import (
    SubscriptionPlanRepository,
)


class SubscriptionPlanRepositoryAdapter(ISeedManyEntries[SubscriptionPlanEntity]):
    """SubscriptionPlanRepositoryAdapter."""

    def __init__(
        self,
        subscription_plan_repository: SubscriptionPlanRepository,
    ):
        """Initialize repository."""
        self._subscription_plan_repository = subscription_plan_repository

    async def add_many(
        self,
        data: list[SubscriptionPlanEntity],
    ) -> Sequence[SubscriptionPlanEntity]:
        """Add many entries."""
        return await self._subscription_plan_repository.add_many(data)

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._subscription_plan_repository.delete_everything()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._subscription_plan_repository.exists_anything()
