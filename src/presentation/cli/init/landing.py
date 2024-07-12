"""Cli commands for initializing the landing."""

import json
import logging
import uuid
from pathlib import Path

import aiofiles
import click
from dishka import AsyncContainer
from dishka import Scope
from litestar import Litestar
from litestar.datastructures import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra import settings
from src.domain.entities.landing import LandingSnippet
from src.domain.entities.landing import LandingSolution
from src.domain.entities.subscriptions import SubscriptionPlan
from src.domain.entities.landing.home_page import LandingHomePage
from src.domain.entities.landing.settings import LandingSettings
from src.application.services.landing_home_page import LandingHomePageService
from src.application.services import LandingSettingsService
from src.application.services import LandingSnippetService
from src.application.services import LandingSolutionService
from src.application.services.subscription_plan import SubscriptionPlanService

logger = logging.getLogger(__name__)


@click.command(
    help="Create all seed data for the application.",
)
@click.pass_obj
def landing(app: Litestar) -> None:
    """Create default seed data."""
    import anyio
    from rich import get_console

    # get the console
    console = get_console()

    async def _create_all_seed_data() -> None:
        console.rule("Loading landing data")
        container: AsyncContainer = app.state.dishka_container
        async with (
            container(scope=Scope.REQUEST) as container,
            await container.get(AsyncSession) as db_session,
        ):
            await load_landing_data(app=app, container=container, db_session=db_session)
            await load_subscription_plans(
                app=app, container=container, db_session=db_session
            )
            await db_session.commit()

    console.rule("Creating seed data")
    # noinspection PyTypeChecker
    anyio.run(_create_all_seed_data)


async def load_landing_data(
    app: Litestar, container: AsyncContainer, db_session: AsyncSession
) -> None:
    """Import/Synchronize Database Fixtures."""
    landing_settings_service: LandingSettingsService = await container.get(
        LandingSettingsService,
    )
    landing_home_page_service: LandingHomePageService = await container.get(
        LandingHomePageService
    )
    landing_solution_service: LandingSolutionService = await container.get(
        LandingSolutionService
    )
    landing_snippet_service: LandingSnippetService = await container.get(
        LandingSnippetService
    )

    # check if no landing setting service exists, if not create a new landing settings
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
    if not await landing_solution_service.exists():
        logger.info("Creating default landing solutions from a fixture")

        # get fixtures data
        solutions_fixtures_path: Path = Path(
            settings.db.fixture_path, "landing_solutions.json"
        )
        fixtures_data: list[dict] = json.loads(solutions_fixtures_path.read_text())

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

    # create landing snippets
    await landing_snippet_service.delete_where()
    if not await landing_snippet_service.exists():
        logger.info("Creating default landing snippets from a fixture")

        # get fixtures data
        snippet_fixtures_path: Path = Path(
            settings.db.fixture_path, "landing_snippets.json"
        )
        snippet_fixtures_data: list[dict] = json.loads(
            snippet_fixtures_path.read_text()
        )

        # prepare landing snippets
        landing_snippets: list[LandingSnippet] = [
            LandingSnippet(**landing_snippet)
            for landing_snippet in snippet_fixtures_data
        ]

        # create landing snippets
        await landing_snippet_service.create_many(landing_snippets)
        logger.info("Default landing snippets created")


async def load_subscription_plans(
    app: Litestar, container: AsyncContainer, db_session: AsyncSession
) -> None:
    """Import/Synchronize Database Fixtures."""
    subscription_plan_service: SubscriptionPlanService = await container.get(
        SubscriptionPlanService
    )

    # check if no subscription plan service exists, create a new subscription plan
    if not await subscription_plan_service.exists():
        logger.info("Creating default subscription plans from a fixture")

        # get fixtures data
        fixtures_path: Path = Path(settings.db.fixture_path, "subscription_plans.json")
        fixtures_data: list[dict] = json.loads(fixtures_path.read_text())

        # prepare subscription plans
        subscription_plans: list[SubscriptionPlan] = [
            SubscriptionPlan(**subscription_plan) for subscription_plan in fixtures_data
        ]

        # create subscription plans
        await subscription_plan_service.create_many(subscription_plans)
        logger.info("Default subscription plans created")
    else:
        logger.info("Default subscription plans already exists")
