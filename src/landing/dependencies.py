"""Dependencies for landing module."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.landing.services.landing_home_page import LandingHomePageService
from src.landing.services.landing_settings import LandingSettingsService
from src.landing.services.landing_solution import LandingSolutionService


async def provide_landing_settings_service(
    db_session: AsyncSession,
) -> AsyncGenerator[LandingSettingsService, None]:
    """Construct repository and service objects for the request."""
    async with LandingSettingsService.new(
        session=db_session,
    ) as service:
        yield service


async def provide_landing_solution_service(
    db_session: AsyncSession,
) -> AsyncGenerator[LandingSolutionService, None]:
    """Construct repository and service objects for the request."""
    async with LandingSolutionService.new(
        session=db_session,
    ) as service:
        yield service


async def provide_landing_home_page_service(
    db_session: AsyncSession,
) -> AsyncGenerator[LandingHomePageService, None]:
    """Construct repository and service objects for the request."""
    async with LandingHomePageService.new(
        session=db_session,
    ) as service:
        yield service
