"""Fixture database loader services."""

from src.common.base.fixture_loader import FixtureDatabaseLoaderService
from src.features.subscriptions.public.entities import SubscriptionPlanEntity
from src.features.users.public.entities import UserEntity


class SubscriptionPlanFixtureDatabaseLoaderService(
    FixtureDatabaseLoaderService[SubscriptionPlanEntity],
):
    """Subscription plan fixture database loader service."""

    entity_class = SubscriptionPlanEntity
    future_name = "subscriptions"


class UserFixtureDatabaseLoaderService(
    FixtureDatabaseLoaderService[UserEntity],
):
    """User fixture database loader service."""

    entity_class = UserEntity
    future_name = "users"
