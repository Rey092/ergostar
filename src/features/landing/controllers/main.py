"""Landing Controller."""

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller
from litestar import get
from litestar.datastructures import CacheControlHeader
from litestar.response import Template

from src.features.landing.interactors.get_faq import GetFaqInteractor
from src.features.landing.interactors.get_home import GetHomeInteractor
from src.features.landing.interactors.get_pricing import GetPricingInteractor


class LandingController(Controller):
    """Landing Controller."""

    @get(
        path="/",
        name="landing:home",
        cache=4 * 60 * 60,  # 4 hours
        cache_control=CacheControlHeader(max_age=4 * 60 * 60),  # 4 hours
    )
    @inject
    async def get_home(
        self,
        get_home_interactor: FromDishka[GetHomeInteractor],
    ) -> Template:
        """Serve site root."""
        context: dict = await get_home_interactor()
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
    async def get_faq(
        self,
        get_faq_interactor: FromDishka[GetFaqInteractor],
    ) -> Template:
        """Serve faq page."""
        context: dict = await get_faq_interactor()
        return Template(
            template_name="landing/pages/faq.html",
            context=context,
        )

    @get(
        path="/pricing",
        name="landing:pricing",
        cache=4 * 60 * 60,  # 4 hours
        cache_control=CacheControlHeader(max_age=4 * 60 * 60),  # 4 hours
    )
    @inject
    async def get_pricing(
        self,
        get_pricing_interactor: FromDishka[GetPricingInteractor],
    ) -> Template:
        """Serve pricing page."""
        context: dict = await get_pricing_interactor()
        # landing_settings: LandingSettings = await landing_settings_service.get_one()
        # available_subscription_plans: Sequence[
        #     SubscriptionPlan
        # ] = await subscription_plan_service.list_available()
        return Template(
            template_name="landing/pages/pricing.html",
            context=context,
            # context={
            # "landing_settings": landing_settings,
            # "subscription_plans": available_subscription_plans,
            # },
        )
