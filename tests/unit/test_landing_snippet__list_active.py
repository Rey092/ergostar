# from collections.abc import AsyncIterable  # noqa
#
# import pytest
# import pytest_asyncio
# from dishka import AsyncContainer
# from dishka import Scope
# from dishka import make_async_container
# from dishka import provide
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from db.models import LandingSnippet
# from src.landing.services.landing_snippet import LandingSnippetService
# from tests.src.provider import MockLandingProvider
# from tests.src.repositories import MockLandingSnippetRepository
#
#
# class MockProvider(MockLandingProvider):
#     """Provide landing snippet service."""
#
#     @provide(scope=Scope.REQUEST)
#     async def landing_snippet_service(
#         self, session: AsyncSession
#     ) -> AsyncIterable[LandingSnippetService]:
#         """Provide landing home page service."""
#         async with LandingSnippetService.new(
#             session=session,
#         ) as service:
#             service.repository = MockLandingSnippetRepository(session=session)
#             yield service
#
#
# @pytest_asyncio.fixture
# async def container() -> AsyncIterable[AsyncContainer]:
#     container: AsyncContainer = make_async_container(MockProvider())
#     async with container(scope=Scope.REQUEST) as container:
#         yield container
#
#
# @pytest.mark.asyncio()
# async def test_list_active(container: AsyncContainer):
#     """Test list active snippets."""
#     service: LandingSnippetService = await container.get(LandingSnippetService)
#     snippets: list[LandingSnippet] = await service.list_active()
#     # assert snippets is really a list of LandingSnippet
#     assert isinstance(snippets, list)
#     assert all(isinstance(snippet, LandingSnippet) for snippet in snippets)
