"""App provider (DI)."""

from collections.abc import AsyncIterable

from dishka import Scope
from dishka import from_context
from dishka import provide
from dishka.provider import Provider
from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import settings


class AppProvider(Provider):
    """Application provider (DI)."""

    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_session_maker(self) -> async_sessionmaker[AsyncSession]:
        """Provide async session maker."""
        return async_sessionmaker(
            settings.db.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        """Provide async session."""
        async with session_maker() as session:
            yield session
