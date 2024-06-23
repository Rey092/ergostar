"""Landing provider (DI)."""

from collections.abc import AsyncIterable

from dishka import Scope
from dishka import from_context
from dishka import provide
from dishka.provider import Provider
from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.landing.services.landing_home_page import LandingHomePageService
from src.landing.services.landing_settings import LandingSettingsService
from src.landing.services.landing_snippet import LandingSnippetService
from src.landing.services.landing_solution import LandingSolutionService


class LandingProvider(Provider):
    """Landing provider (DI)."""

    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def landing_settings_service(
        self, session: AsyncSession
    ) -> AsyncIterable[LandingSettingsService]:
        """Provide landing home page service."""
        async with LandingSettingsService.new(
            session=session,
        ) as service:
            yield service

    @provide(scope=Scope.REQUEST)
    async def landing_home_page_service(
        self, session: AsyncSession
    ) -> AsyncIterable[LandingHomePageService]:
        """Provide landing home page service."""
        async with LandingHomePageService.new(
            session=session,
        ) as service:
            yield service

    @provide(scope=Scope.REQUEST)
    async def landing_solution_service(
        self, session: AsyncSession
    ) -> AsyncIterable[LandingSolutionService]:
        """Provide landing home page service."""
        async with LandingSolutionService.new(
            session=session,
        ) as service:
            yield service

    @provide(scope=Scope.REQUEST)
    async def landing_snippet_service(
        self, session: AsyncSession
    ) -> AsyncIterable[LandingSnippetService]:
        """Provide landing home page service."""
        async with LandingSnippetService.new(
            session=session,
        ) as service:
            yield service
