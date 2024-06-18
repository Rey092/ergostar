"""Cli commands for initializing the application."""

from __future__ import annotations

import json
import logging
import uuid
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

import aiofiles
import click
from litestar.datastructures import UploadFile

from config import settings
from db.models import LandingHomePage
from db.models import LandingSettings
from db.models import LandingSolution
from src.landing.dependencies import provide_landing_home_page_service
from src.landing.dependencies import provide_landing_solution_service

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.landing.services.landing_home_page import LandingHomePageService
    from src.landing.services.landing_settings import LandingSettingsService
    from src.landing.services.landing_solution import LandingSolutionService

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
    landing_solution_service: LandingSolutionService = await anext(
        provide_landing_solution_service(db_session)
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

    # check if no landing setting service exists, create a new lending solutions
    await landing_solution_service.delete_where()
    if not await landing_solution_service.exists():
        logger.info("Creating default landing solutions from a fixture")

        # get fixtures data
        fixtures_path: Path = Path(settings.db.FIXTURE_PATH, "landing_solutions.json")
        fixtures_data: list[dict] = json.loads(fixtures_path.read_text())

        # get image data
        test_image_path: Path = Path(settings.app.BASE_DIR, "seed", "img", "test.png")
        async with aiofiles.open(test_image_path, "rb") as f:
            test_image_data: bytes = await f.read()

        # prepare landing solutions
        landing_solutions: list[LandingSolution] = [
            LandingSolution(
                **landing_solution,
                docs_url="https://docs.example.com",
                file=UploadFile(
                    content_type="image/png",
                    filename=f"file_{uuid.uuid4()}.png",
                    file_data=test_image_data,
                ),
            )
            for landing_solution in fixtures_data
        ]

        # create landing solutions
        await landing_solution_service.create_many(landing_solutions)
        logger.info("Default landing solutions created")


@init_project_app.command(
    name="create-all",
    help="Create all seed data for the application.",
)
def create_all_seed_data() -> None:
    """Create default seed data."""
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
    # noinspection PyTypeChecker
    anyio.run(_create_all_seed_data)
