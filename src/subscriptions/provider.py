"""Subscription provider (DI)."""

from collections.abc import AsyncIterable

from dishka import Scope
from dishka import provide
from dishka.provider import Provider
from sqlalchemy.ext.asyncio import AsyncSession

from src.landing.services.subscription_plan import SubscriptionPlanService


class SubscriptionProvider(Provider):
    """Subscription provider (DI)."""

    @provide(scope=Scope.REQUEST)
    async def get_subscription_plan_service(
        self, session: AsyncSession
    ) -> AsyncIterable[SubscriptionPlanService]:
        """Provide subscriptions home page service."""
        async with SubscriptionPlanService.new(
            session=session,
        ) as service:
            yield service
