"""SubscriptionPlanRepositoryAdapter."""

from collections.abc import Sequence

from src.common.base.repositories.alchemy import AlchemyAdapterRepository
from src.common.base.repositories.alchemy import GenericAlchemyRepository
from src.common.interfaces.fixture_loader.repository import ISeedRepository
from src.features.subscriptions.public.entities import SubscriptionPlanEntity
from src.features.subscriptions.public.interfaces import (
    ISubscriptionPlanRepositoryContract,
)


class SubscriptionPlanRepositoryAdapter(
    AlchemyAdapterRepository[
        SubscriptionPlanEntity,
        ISubscriptionPlanRepositoryContract[SubscriptionPlanEntity],
    ],
    ISeedRepository[SubscriptionPlanEntity],
):
    """SubscriptionPlanRepositoryAdapter."""

    entity_type = SubscriptionPlanEntity
    repository_type = GenericAlchemyRepository[SubscriptionPlanEntity]

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
