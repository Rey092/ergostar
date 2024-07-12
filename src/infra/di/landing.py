"""Landing provider (DI)."""

from collections.abc import AsyncIterable

from dishka import Scope
from dishka import provide
from dishka.provider import Provider
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interactors.landing.get_home_page_context import GetHomePageContextInteractor
from src.application.services.landing_home_page import LandingHomePageService
from src.application.services import LandingSettingsService
from src.application.services import LandingSnippetService
from src.application.services import LandingSolutionService


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
