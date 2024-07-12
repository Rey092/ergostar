"""Landing provider (DI)."""

from dishka import Scope
from dishka import provide
from dishka.provider import Provider

from src.landing.interactors.get_home_page_context import GetHomePageContextInteractor


class LandingProvider(Provider):
    """Landing provider (DI)."""
    #
    # @provide(scope=Scope.REQUEST)
    # async def landing_settings_service(
    #     self, session: AsyncSession
    # ) -> AsyncIterable[LandingSettingsService]:
    #     """Provide landing home page service."""
    #     async with LandingSettingsService.new(
    #         session=session,
    #     ) as service:
    #         yield service
    #
    # @provide(scope=Scope.REQUEST)
    # async def landing_home_page_service(
    #     self, session: AsyncSession
    # ) -> AsyncIterable[LandingHomePageService]:
    #     """Provide landing home page service."""
    #     async with LandingHomePageService.new(
    #         session=session,
    #     ) as service:
    #         yield service
    #
    # @provide(scope=Scope.REQUEST)
    # async def landing_solution_service(
    #     self, session: AsyncSession
    # ) -> AsyncIterable[LandingSolutionService]:
    #     """Provide landing home page service."""
    #     async with LandingSolutionService.new(
    #         session=session,
    #     ) as service:
    #         yield service
    #
    # @provide(scope=Scope.REQUEST)
    # async def landing_snippet_service(
    #     self, session: AsyncSession
    # ) -> AsyncIterable[LandingSnippetService]:
    #     """Provide landing home page service."""
    #     async with LandingSnippetService.new(
    #         session=session,
    #     ) as service:
    #         yield service
    #
    get_landing_home_page_context_interactor = provide(source=GetHomePageContextInteractor, scope=Scope.REQUEST)
