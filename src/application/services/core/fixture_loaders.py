"""Fixture database loader services."""

from src.application.common.fixture_loader import FixtureDatabaseLoaderService
from src.domain.entities.subscriptions import SubscriptionPlan
from src.domain.entities.users import User


class SubscriptionPlanFixtureDatabaseLoaderService(
    FixtureDatabaseLoaderService[SubscriptionPlan],
):
    """Subscription plan fixture database loader service."""

    entity_class = SubscriptionPlan


class UserFixtureDatabaseLoaderService(
    FixtureDatabaseLoaderService[User],
):
    """User fixture database loader service."""

    entity_class = User
