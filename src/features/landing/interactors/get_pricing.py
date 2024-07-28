"""GetPricingInteractor."""
from src.features.landing.entities import (
    LandingSettings
)
from src.features.subscriptions.entities import SubscriptionPlan
from src.features.landing.interactors import interfaces


class GetPricingInteractor:
    """Get pricing page interactor."""

    def __init__(
        self,
        landing_settings_repository: interfaces.IGetOneLandingSettings,
        subscription_plan_repository: interfaces.IListPublicSubscriptionPlans,
    ):
        """Initialize the interactor."""
        self._landing_settings_repository = landing_settings_repository
        self._subscription_plan_repository = subscription_plan_repository

    async def __call__(self) -> dict:
        """Execute the interactor."""
        landing_settings: LandingSettings = await self._landing_settings_repository.get_one()
        subscription_plans: list[SubscriptionPlan] = await self._subscription_plan_repository.list_public()

        return {
            "landing_settings": landing_settings,
            "subscription_plans": subscription_plans,
        }
