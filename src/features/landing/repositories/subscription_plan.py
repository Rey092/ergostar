"""Landing settings repository."""
from src.common.base.alchemy import AlchemyRepository
from src.features.landing.interactors.interfaces import IListPublicSubscriptionPlans
from src.features.subscriptions import SubscriptionPlan


class LandingSubscriptionPlansRepository(
    AlchemyRepository[SubscriptionPlan],
    IListPublicSubscriptionPlans
):
    """
    LandingSettingsRepository.

    This repository is responsible for handling the SubscriptionPlan entity.
    Composition with "SubscriptionPlansRepository" from "subscriptions"
    feature is not necessary for this repository right now.
    """

    model_type = SubscriptionPlan

    async def list_public(self) -> list[SubscriptionPlan]:
        """List public subscription plans."""
        return await self._repository.list(is_public=True)
