"""GetHomeInteractor interactor."""
from typing import Sequence
from src.features.landing.entities import (
    LandingSettings,
    LandingHomePage,
    LandingSolution,
    LandingSnippet
)
from . import interfaces


class GetHomeInteractor:
    """Get home page interactor."""

    def __init__(
        self,
        landing_settings_repository: interfaces.IGetOneLandingSettings,
        landing_home_page_repository: interfaces.IGetOneLandingHomePage,
        landing_solution_repository: interfaces.IGetCarouserLandingSolutions,
        landing_snippet_repository: interfaces.IListActiveLandingSnippets,
    ):
        """Initialize the interactor."""
        self._landing_settings_repository = landing_settings_repository
        self._landing_home_page_repository = landing_home_page_repository
        self._landing_solution_repository = landing_solution_repository
        self._landing_snippet_repository = landing_snippet_repository

    async def __call__(self) -> dict:
        """Execute the interactor."""
        landing_settings: LandingSettings = await self._landing_settings_repository.get_one()

        landing_home_page: LandingHomePage = await self._landing_home_page_repository.get_one()

        landing_snippets: list[LandingSnippet] = await self._landing_snippet_repository.list_active()

        landing_solutions_top_banners: list[LandingSolution] = await self._landing_solution_repository.list_top_banners()

        landing_solutions_carousel: list[LandingSolution] = (
            await self._landing_solution_repository.list_active_solutions_for_carousel()
        )

        landing_solutions_carousel_string: str = ", ".join(
            [f'"{service.title_carousel}"' for service in landing_solutions_carousel]
        )

        return {
            "landing_settings": landing_settings,
            "landing_home_page": landing_home_page,
            "landing_snippets": landing_snippets,
            "landing_solutions_top_banners": landing_solutions_top_banners,
            "landing_solutions_carousel_string": landing_solutions_carousel_string,
        }
