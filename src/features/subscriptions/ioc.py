"""Subscription provider (DI)."""

from dishka import Scope
from dishka import provide
from dishka.provider import Provider

from src.features.subscriptions.public.interfaces import (
    ISubscriptionPlanRepositoryContract,
)
from src.features.subscriptions.repositories.subscription_plan import (
    SubscriptionPlanRepository,
)


class SubscriptionsProvider(Provider):
    """Subscription provider (DI)."""

    get_subscription_plan_repository = provide(
        source=SubscriptionPlanRepository,
        scope=Scope.REQUEST,
        provides=ISubscriptionPlanRepositoryContract,
    )
