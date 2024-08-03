"""Gateway for Subscriptions feature."""

from src.common.base.gateway import AlchemyGateway
from src.common.base.repository import GenericSQLAlchemyRepository
from src.features.subscriptions import SubscriptionPlan


class SubscriptionPlanGateway(AlchemyGateway[SubscriptionPlan]):
    """Subscription Plan gateway."""

    model_type = SubscriptionPlan
    repository_type = GenericSQLAlchemyRepository[SubscriptionPlan]
