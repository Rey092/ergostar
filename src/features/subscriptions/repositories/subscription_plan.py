"""Repository for subscription plan feature."""

from collections.abc import Sequence

from src.common.base.repositories.alchemy import AlchemyMappedRepository
from src.common.base.repositories.alchemy import GenericSQLAlchemyRepository
from src.features.subscriptions import SubscriptionPlanModel
from src.features.subscriptions.entities import SubscriptionPlanEntity


class SubscriptionPlanRepository(
    AlchemyMappedRepository[SubscriptionPlanEntity, SubscriptionPlanModel],
):
    """Subscription Plan repository."""

    model_type = SubscriptionPlanModel
    repository_type = GenericSQLAlchemyRepository[SubscriptionPlanModel]

    async def add_many(
        self,
        data: list[SubscriptionPlanEntity],
    ) -> Sequence[SubscriptionPlanEntity]:
        """Add many entries."""
        models = [self.entity_to_model(item) for item in data]
        entities = await self._repository.add_many(models)
        return [self.model_to_entity(item) for item in entities]

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._repository.delete_where()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._repository.exists()
