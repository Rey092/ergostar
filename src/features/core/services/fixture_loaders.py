"""Fixture database loader services."""

from src.common.base.fixture_loader import FixtureDatabaseLoaderService
from src.features.subscriptions.entities import SubscriptionPlan
from src.features.users.entities import User


class SubscriptionPlanFixtureDatabaseLoaderService(
    FixtureDatabaseLoaderService[SubscriptionPlan],
):
    """Subscription plan fixture database loader service."""

    entity_class = SubscriptionPlan
    future_name = "subscriptions"


class UserFixtureDatabaseLoaderService(
    FixtureDatabaseLoaderService[User],
):
    """User fixture database loader service."""

    entity_class = User
    future_name = "users"
