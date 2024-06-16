from litestar import Controller, get
from litestar.datastructures import CacheControlHeader
from litestar.di import Provide
from litestar.response import Template
from db.models import LandingSettings, LandingHomePage
from src.landing.dependencies import (
    provide_landing_settings_service,
    provide_landing_home_page_service,
)
from src.landing.services.home_page import LandingHomePageService
from src.landing.services.landing_settings import LandingSettingsService


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
            "landing_home_page_service": Provide(provide_landing_home_page_service)
        },
        cache=4 * 60 * 60,  # 4 hours
        cache_control=CacheControlHeader(max_age=4 * 60 * 60),  # 4 hours
    )
    async def get_home(
        self,
        landing_settings_service: LandingSettingsService,
        landing_home_page_service: LandingHomePageService,
    ) -> Template:
        """Serve site root."""
        landing_settings: LandingSettings = await landing_settings_service.get_one()
        home_page: LandingHomePage = await landing_home_page_service.get_one()
        return Template(
            template_name="landing/pages/home.html",
            context={
                "landing_settings": landing_settings,
                "home_page": home_page,
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
