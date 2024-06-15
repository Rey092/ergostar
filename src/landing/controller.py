from litestar import Controller, get
from litestar.di import Provide
from litestar.response import Template
from litestar.status_codes import HTTP_200_OK
from config import constants
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
        path=[constants.SITE_INDEX, f"{constants.SITE_INDEX}/{{path:str}}"],
        name="landing:home",
        status_code=HTTP_200_OK,
        dependencies={
            "landing_home_page_service": Provide(provide_landing_home_page_service)
        },
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
