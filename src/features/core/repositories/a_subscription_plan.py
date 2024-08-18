"""SubscriptionPlanRepositoryAdapter."""

from collections.abc import Sequence

from src.common.base.repositories.alchemy import AlchemyAdapterRepository
from src.common.base.repositories.alchemy import GenericAlchemyRepository
from src.common.interfaces.fixture_loader.repository import ISeedManyEntries
from src.features.subscriptions import SubscriptionPlanModel
from src.features.subscriptions.entities import SubscriptionPlanEntity
from src.features.subscriptions.repositories.subscription_plan import (
    SubscriptionPlanRepository,
)


class SubscriptionPlanRepositoryAdapter(
    AlchemyAdapterRepository[
        SubscriptionPlanEntity,
        SubscriptionPlanModel,
        SubscriptionPlanRepository,
    ],
    ISeedManyEntries[SubscriptionPlanEntity],
):
    """SubscriptionPlanRepositoryAdapter."""

    model_type = SubscriptionPlanModel
    repository_type = GenericAlchemyRepository[SubscriptionPlanModel]

    async def add_many(
        self,
        data: list[SubscriptionPlanEntity],
    ) -> Sequence[SubscriptionPlanEntity]:
        """Add many entries."""
        return await self._adaptee.add_many(data)

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._adaptee.delete_everything()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._adaptee.exists_anything()
