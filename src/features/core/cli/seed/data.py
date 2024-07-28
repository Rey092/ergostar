"""Cli commands for initializing the landing."""
import asyncio
import logging
import click
from dishka import AsyncContainer
from dishka import Scope
from litestar import Litestar
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.landing.interactors.seed.landing_settings import SeedLandingSettingsInteractor

logger = logging.getLogger(__name__)


@click.command(
    help="Create all seed data for the application.",
)
@click.pass_obj
def data(app: Litestar) -> None:
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
            # await container.get(AsyncSession) as db_session,
        ):
            # get interactors
            seed_landing_settings = await container.get(SeedLandingSettingsInteractor)

            # seed data
            await seed_landing_settings()

    console.rule("Creating seed data")
    asyncio.run(_create_all_seed_data())
    console.rule("Seed data created")


# async def load_landing_data(
#     app: Litestar, container: AsyncContainer, db_session: AsyncSession
# ) -> None:
#     """Import/Synchronize Database Fixtures."""
#     landing_settings_repository: LandingSettingsRepository = await container.get(
#         LandingSettingsRepository,
#     )
#     landing_home_page_repository: LandingHomePageRepository = await container.get(
#         LandingHomePageRepository
#     )
#     landing_solution_repository: LandingSolutionRepository = await container.get(
#         LandingSolutionRepository
#     )
#     landing_snippet_repository: LandingSnippetRepository = await container.get(
#         LandingSnippetRepository
#     )
#     # check if no home page exists, create a new home page
#     if not await landing_home_page_repository.exists():
#         logger.info("Creating default home page")
#         await landing_home_page_repository.create(LandingHomePage())
#         logger.info("Default home page created")
#     else:
#         logger.info("Default home page already exists")
#
#     # check if no landing setting service exists, create a new lending solutions
#     if not await landing_solution_repository.exists():
#         logger.info("Creating default landing solutions from a fixture")
#
#         # get fixtures data
#         solutions_fixtures_path: Path = Path(
#             settings.db.fixture_path, "landing_solutions.json"
#         )
#         fixtures_data: list[dict] = json.loads(solutions_fixtures_path.read_text())
#
#         # get image data
#         test_image_path: Path = Path(settings.app.BASE_DIR, "seed", "img", "test.png")
#         async with aiofiles.open(test_image_path, "rb") as f:
#             test_image_data: bytes = await f.read()
#
#         # prepare landing solutions
#         landing_solutions: list[LandingSolution] = [
#             LandingSolution(
#                 **landing_solution,
#                 docs_url="https://docs.example.com",
#                 file=UploadFile(
#                     content_type="image/png",
#                     filename=f"file_{uuid.uuid4()}.png",
#                     file_data=test_image_data,
#                 ),
#             )
#             for landing_solution in fixtures_data
#         ]
#
#         # create landing solutions
#         await landing_solution_repository.create_many(landing_solutions)
#         logger.info("Default landing solutions created")
#
#     # create landing snippets
#     await landing_snippet_repository.delete_where()
#     if not await landing_snippet_repository.exists():
#         logger.info("Creating default landing snippets from a fixture")
#
#         # get fixtures data
#         snippet_fixtures_path: Path = Path(
#             settings.db.fixture_path, "landing_snippets.json"
#         )
#         snippet_fixtures_data: list[dict] = json.loads(
#             snippet_fixtures_path.read_text()
#         )
#
#         # prepare landing snippets
#         landing_snippets: list[LandingSnippet] = [
#             LandingSnippet(**landing_snippet)
#             for landing_snippet in snippet_fixtures_data
#         ]
#
#         # create landing snippets
#         await landing_snippet_repository.add_many(landing_snippets)
#         logger.info("Default landing snippets created")
#
#
# async def load_subscription_plans(
#     app: Litestar, container: AsyncContainer, db_session: AsyncSession
# ) -> None:
#     """Import/Synchronize Database Fixtures."""
#     subscription_plan_service: SubscriptionPlanService = await container.get(
#         SubscriptionPlanService
#     )
#
#     # check if no subscription plan service exists, create a new subscription plan
#     if not await subscription_plan_service.exists():
#         logger.info("Creating default subscription plans from a fixture")
#
#         # get fixtures data
#         fixtures_path: Path = Path(settings.db.fixture_path, "subscription_plans.json")
#         fixtures_data: list[dict] = json.loads(fixtures_path.read_text())
#
#         # prepare subscription plans
#         subscription_plans: list[SubscriptionPlan] = [
#             SubscriptionPlan(**subscription_plan) for subscription_plan in fixtures_data
#         ]
#
#         # create subscription plans
#         await subscription_plan_service.create_many(subscription_plans)
#         logger.info("Default subscription plans created")
#     else:
#         logger.info("Default subscription plans already exists")
