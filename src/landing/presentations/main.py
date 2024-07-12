"""Landing Controller."""

from typing import TYPE_CHECKING

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller
from litestar import get
from litestar.datastructures import CacheControlHeader
from litestar.response import Template

from src.landing.interactors.get_home_page_context import GetHomePageContextInteractor

if TYPE_CHECKING:
    pass


class LandingController(Controller):
    """Landing Controller."""

    include_in_schema = False
    opt = {"exclude_from_auth": True}

    @get(
        path="/",
        name="landing:home",
        cache=4 * 60 * 60,  # 4 hours
        cache_control=CacheControlHeader(max_age=4 * 60 * 60),  # 4 hours
    )
    @inject
    async def get_home(
        self,
        get_home_page_context_interactor: FromDishka[GetHomePageContextInteractor],
    ) -> Template:
        """Serve site root."""
        context: dict = await get_home_page_context_interactor()
        return Template(
            template_name="landing/pages/home.html",
            context=context,
        )

    @get(
        path="/faq",
        name="landing:faq",
        cache=4 * 60 * 60,  # 4 hours
        cache_control=CacheControlHeader(max_age=4 * 60 * 60),  # 4 hours
    )
    @inject
    async def faq(
        self,
        # landing_settings_service: FromDishka[LandingSettingsService],
    ) -> Template:
        """Serve faq page."""
        # landing_settings: LandingSettings = await landing_settings_service.get_one()
        return Template(
            template_name="landing/pages/faq.html",
            context={
                # "landing_settings": landing_settings,
            },
        )

    @get(
        path="/pricing",
        name="landing:pricing",
        cache=4 * 60 * 60,  # 4 hours
        cache_control=CacheControlHeader(max_age=4 * 60 * 60),  # 4 hours
    )
    @inject
    async def pricing(
        self,
        # landing_settings_service: FromDishka[LandingSettingsService],
        # subscription_plan_service: FromDishka[SubscriptionPlanService],
    ) -> Template:
        """Serve pricing page."""
        # landing_settings: LandingSettings = await landing_settings_service.get_one()
        # available_subscription_plans: Sequence[
        #     SubscriptionPlan
        # ] = await subscription_plan_service.list_available()
        return Template(
            template_name="landing/pages/pricing.html",
            context={
                # "landing_settings": landing_settings,
                # "subscription_plans": available_subscription_plans,
            },
        )
