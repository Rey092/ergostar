"""SubscriptionPlanGatewayAdapter."""

from collections.abc import Sequence

from src.features.core.services.interfaces import ISeedManyEntries
from src.features.subscriptions.entities import SubscriptionPlan
from src.features.subscriptions.gateways import SubscriptionPlanGateway


class SubscriptionPlanGatewayAdapter(ISeedManyEntries[SubscriptionPlan]):
    """SubscriptionPlanGatewayAdapter."""

    def __init__(
        self,
        subscription_plan_gateway: SubscriptionPlanGateway,
    ):
        """Initialize gateway."""
        self._subscription_plan_gateway = subscription_plan_gateway

    async def add_many(
        self,
        data: list[SubscriptionPlan],
    ) -> Sequence[SubscriptionPlan]:
        """Add many entries."""
        return await self._subscription_plan_gateway.add_many(data)

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._subscription_plan_gateway.delete_everything()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._subscription_plan_gateway.exists_anything()
