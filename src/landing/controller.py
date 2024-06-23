"""Landing Controller."""

from typing import TYPE_CHECKING

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller
from litestar import get
from litestar.datastructures import CacheControlHeader
from litestar.response import Template

from src.landing.services.landing_home_page import LandingHomePageService
from src.landing.services.landing_settings import LandingSettingsService
from src.landing.services.landing_snippet import LandingSnippetService
from src.landing.services.landing_solution import LandingSolutionService
from src.subscriptions.services.subscription_plan import SubscriptionPlanService

if TYPE_CHECKING:
    from collections.abc import Sequence

    from db.models import LandingHomePage
    from db.models import LandingSettings
    from db.models import LandingSnippet
    from db.models import LandingSolution
    from db.models import SubscriptionPlan


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
        landing_settings_service: FromDishka[LandingSettingsService],
        landing_home_page_service: FromDishka[LandingHomePageService],
        landing_solution_service: FromDishka[LandingSolutionService],
        landing_snippet_service: FromDishka[LandingSnippetService],
    ) -> Template:
        """Serve site root."""
        landing_settings: LandingSettings = await landing_settings_service.get_one()
        landing_home_page: LandingHomePage = await landing_home_page_service.get_one()
        landing_solutions_carousel_string: str = (
            await landing_solution_service.get_carousel_string()
        )
        landing_solutions_top_banners: Sequence[
            LandingSolution
        ] = await landing_solution_service.list_top_banners()
        landing_snippets: Sequence[
            LandingSnippet
        ] = await landing_snippet_service.list_active()
        return Template(
            template_name="landing/pages/home.html",
            context={
                "landing_settings": landing_settings,
                "landing_solutions_carousel_string": landing_solutions_carousel_string,
                "landing_solutions_top_banners": landing_solutions_top_banners,
                "landing_home_page": landing_home_page,
                "landing_snippets": landing_snippets,
            },
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
        landing_settings_service: FromDishka[LandingSettingsService],
    ) -> Template:
        """Serve site root."""
        landing_settings: LandingSettings = await landing_settings_service.get_one()
        return Template(
            template_name="landing/pages/faq.html",
            context={
                "landing_settings": landing_settings,
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
        landing_settings_service: FromDishka[LandingSettingsService],
        subscription_plan_service: FromDishka[SubscriptionPlanService],
    ) -> Template:
        """Serve site root."""
        landing_settings: LandingSettings = await landing_settings_service.get_one()
        available_subscription_plans: Sequence[
            SubscriptionPlan
        ] = await subscription_plan_service.list_available()
        return Template(
            template_name="landing/pages/pricing.html",
            context={
                "landing_settings": landing_settings,
                "subscription_plans": available_subscription_plans,
            },
        )
