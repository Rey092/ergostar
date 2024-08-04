"""Gateway for sbscriptions plan feature."""

from collections.abc import Sequence

from src.common.base.gateway import AlchemyGateway
from src.common.base.repository import GenericSQLAlchemyRepository
from src.features.subscriptions import SubscriptionPlanModel
from src.features.subscriptions.entities import SubscriptionPlan


class SubscriptionPlanGateway(AlchemyGateway[SubscriptionPlan, SubscriptionPlanModel]):
    """Subscription Plan gateway."""

    model_type = SubscriptionPlanModel
    repository_type = GenericSQLAlchemyRepository[SubscriptionPlanModel]

    async def add_many(
        self,
        data: list[SubscriptionPlan],
    ) -> Sequence[SubscriptionPlan]:
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
