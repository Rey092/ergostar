"""Fixture database loader services."""

from src.application.interfaces.repositories.fixture_loaders import (
    IEntityFixtureRepository,
)
from src.domain.entities.subscriptions import SubscriptionPlan
from src.domain.entities.users import User
from src.infrastructure.disk.repositories.common import EntityFixtureRepository


class SubscriptionPlanFixtureRepository(
    EntityFixtureRepository[SubscriptionPlan],
    IEntityFixtureRepository[SubscriptionPlan],
):
    """Subscription plan fixture database loader service."""

    entity_class = SubscriptionPlan


class UserFixtureRepository(
    EntityFixtureRepository[User],
    IEntityFixtureRepository[User],
):
    """User fixture database loader service."""

    entity_class = User
