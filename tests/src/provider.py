"""Landing provider (DI)."""

from collections.abc import AsyncIterable
from unittest.mock import Mock

from dishka import Scope
from dishka import from_context
from dishka import provide
from dishka.provider import Provider
from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession

from tests.src.services import MockLandingHomePageService
from tests.src.services import MockLandingSettingsService
from tests.src.services import MockLandingSnippetService
from tests.src.services import MockLandingSolutionService


class MockLandingProvider(Provider):
    """Base landing provider (DI)."""

    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncIterable[AsyncSession]:
        """Provide async session."""
        connection = Mock()
        yield connection

    @provide(scope=Scope.REQUEST)
    async def landing_settings_service(
        self, session: AsyncSession
    ) -> AsyncIterable[MockLandingSettingsService]:
        """Provide landing home page service."""
        async with MockLandingSettingsService.new(
            session=session,
        ) as service:
            yield service

    @provide(scope=Scope.REQUEST)
    async def landing_home_page_service(
        self, session: AsyncSession
    ) -> AsyncIterable[MockLandingHomePageService]:
        """Provide landing home page service."""
        async with MockLandingHomePageService.new(
            session=session,
        ) as service:
            yield service

    @provide(scope=Scope.REQUEST)
    async def landing_solution_service(
        self, session: AsyncSession
    ) -> AsyncIterable[MockLandingSolutionService]:
        """Provide landing home page service."""
        async with MockLandingSolutionService.new(
            session=session,
        ) as service:
            yield service

    @provide(scope=Scope.REQUEST)
    async def landing_snippet_service(
        self, session: AsyncSession
    ) -> AsyncIterable[MockLandingSnippetService]:
        """Provide landing home page service."""
        async with MockLandingSnippetService.new(
            session=session,
        ) as service:
            yield service
