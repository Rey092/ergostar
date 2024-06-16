from typing import Sequence
from litestar import Controller, get
from litestar.datastructures import CacheControlHeader
from litestar.di import Provide
from litestar.response import Template
from db.models import LandingSettings, LandingHomePage, LandingSolution
from src.landing.dependencies import (
    provide_landing_settings_service,
    provide_landing_home_page_service,
    provide_landing_solution_service,
)
from src.landing.services.landing_home_page import LandingHomePageService
from src.landing.services.landing_settings import LandingSettingsService
from src.landing.services.landing_solution import LandingSolutionService


class LandingController(Controller):
    """Landing Controller."""

    include_in_schema = False
    opt = {"exclude_from_auth": True}
    dependencies = {
        "landing_settings_service": Provide(provide_landing_settings_service)
    }

    @get(
        path="/",
        name="landing:home",
        dependencies={
            "landing_home_page_service": Provide(provide_landing_home_page_service),
            "landing_solution_service": Provide(provide_landing_solution_service),
        },
        # cache=4 * 60 * 60,  # 4 hours
        # cache_control=CacheControlHeader(max_age=4 * 60 * 60),  # 4 hours
    )
    async def get_home(
        self,
        landing_settings_service: LandingSettingsService,
        landing_home_page_service: LandingHomePageService,
        landing_solution_service: LandingSolutionService,
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
        return Template(
            template_name="landing/pages/home.html",
            context={
                "landing_settings": landing_settings,
                "landing_solutions_carousel_string": landing_solutions_carousel_string,
                "landing_solutions_top_banners": landing_solutions_top_banners,
                "landing_home_page": landing_home_page,
            },
        )

    @get(
        path="/faq",
        name="landing:faq",
        cache=4 * 60 * 60,  # 4 hours
        cache_control=CacheControlHeader(max_age=4 * 60 * 60),  # 4 hours
    )
    async def faq(
        self,
        landing_settings_service: LandingSettingsService,
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
    async def pricing(
        self,
        landing_settings_service: LandingSettingsService,
    ) -> Template:
        """Serve site root."""
        landing_settings: LandingSettings = await landing_settings_service.get_one()
        return Template(
            template_name="landing/pages/pricing.html",
            context={
                "landing_settings": landing_settings,
            },
        )
