from typing import Sequence

from src.application.services import LandingSettingsService, LandingHomePageService, LandingSolutionService, \
    LandingSnippetService
from src.domain.entities.landing import LandingSettings, LandingHomePage, LandingSolution, LandingSnippet


class GetHomePageContextInteractor:
    """Get home page interactor."""

    def __init__(
        self,
        # landing_settings_service: LandingSettingsService,
        # landing_home_page_service: LandingHomePageService,
        # landing_solution_service: LandingSolutionService,
        # landing_snippet_service: LandingSnippetService,
    ):
        """Initialize the interactor."""
        # self.landing_settings_service = landing_settings_service
        # self.landing_home_page_service = landing_home_page_service
        # self.landing_solution_service = landing_solution_service
        # self.landing_snippet_service = landing_snippet_service

    async def __call__(self) -> dict:
        """Execute the interactor."""
        # landing_settings: LandingSettings = await self.landing_settings_service.get_one()
        #
        # landing_home_page: LandingHomePage = await self.landing_home_page_service.get_one()
        #
        # landing_solutions_carousel_string: str = (
        #     await self.landing_solution_service.get_carousel_string()
        # )
        #
        # landing_solutions_top_banners: Sequence[
        #     LandingSolution
        # ] = await self.landing_solution_service.list_top_banners()
        #
        # landing_snippets: Sequence[
        #     LandingSnippet
        # ] = await self.landing_snippet_service.list_active()
        #
        # return {
        #     "landing_settings": landing_settings,
        #     "landing_solutions_carousel_string": landing_solutions_carousel_string,
        #     "landing_solutions_top_banners": landing_solutions_top_banners,
        #     "landing_home_page": landing_home_page,
        #     "landing_snippets": landing_snippets,
        # }

        return {
            "landing_settings": None,
            "landing_solutions_carousel_string": "",
            "landing_solutions_top_banners": [],
            "landing_home_page": None,
            "landing_snippets": [],
        }
