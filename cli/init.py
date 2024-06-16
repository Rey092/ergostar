"""Cli commands for initializing the application."""

from __future__ import annotations

import logging
from typing import Any
import click
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import LandingSettings, LandingHomePage
from src.landing.dependencies import provide_landing_home_page_service
from src.landing.services.home_page import LandingHomePageService
from src.landing.services.landing_settings import LandingSettingsService


logger = logging.getLogger(__name__)


@click.group(
    name="init",
    invoke_without_command=False,
    help="Create seed data for the application.",
)
@click.pass_context
def init_project_app(_: dict[str, Any]) -> None:
    """Manage application users."""


async def load_landing_data(db_session: AsyncSession) -> None:
    """Import/Synchronize Database Fixtures."""

    from src.landing.dependencies import provide_landing_settings_service

    landing_settings_service: LandingSettingsService = await anext(
        provide_landing_settings_service(db_session)
    )
    landing_home_page_service: LandingHomePageService = await anext(
        provide_landing_home_page_service(db_session)
    )

    # check if no landing setting service exists, create a new lending setting
    if not await landing_settings_service.exists():
        logger.info("Creating default landing settings")
        await landing_settings_service.create(LandingSettings())
        logger.info("Default landing settings created")
    else:
        logger.info("Default landing settings already exists")

    # check if no home page exists, create a new home page
    if not await landing_home_page_service.exists():
        logger.info("Creating default home page")
        await landing_home_page_service.create(LandingHomePage())
        logger.info("Default home page created")
    else:
        logger.info("Default home page already exists")


@init_project_app.command(
    name="create-all",
    help="Create all seed data for the application.",
)
def create_all_seed_data() -> None:
    """
    Create default seed data
    """
    import anyio
    from rich import get_console
    from config.plugins import alchemy

    # get the console
    console = get_console()

    async def _create_all_seed_data() -> None:
        async with alchemy.get_session() as db_session:
            console.rule("Loading landing data")
            await load_landing_data(db_session=db_session)
            await db_session.commit()

    console.rule("Creating seed data")
    anyio.run(_create_all_seed_data)  # type: ignore
