"""Subscription provider (DI)."""

from dishka import Scope
from dishka import provide
from dishka.provider import Provider

from src.features.subscriptions.gateways import SubscriptionPlanGateway


class SubscriptionsProvider(Provider):
    """Subscription provider (DI)."""

    get_subscription_plan_gateway = provide(
        source=SubscriptionPlanGateway,
        scope=Scope.REQUEST,
    )
