"""Drop all data."""

import asyncio

import click
from dishka import Scope
from litestar import Litestar

from src.application.interactors.database.drop_database import DropDatabaseInteractor
from src.application.interactors.database.seed_database import SeedDatabaseInteractor
from src.application.interactors.database.seed_database import SeedDatabaseRequestModel
from src.domain.enums.database import DatabaseSeedingGroups


@click.group(
    name="core",
    invoke_without_command=False,
    help="Core methods for the application. Database seeding, dropping, etc.",
)
@click.pass_context
def core_controller(context: click.Context, app: Litestar) -> None:
    """Manage application users."""
    context.obj = app


@click.command(
    help="Drop all data in the database.",
)
@click.confirmation_option(prompt="Are you sure you want to drop the db?")
@click.pass_obj
def drop_db(app: Litestar) -> None:
    """Drop all data in the database."""
    from rich import get_console

    # get the console
    console = get_console()

    async def _drop_database_tables() -> None:
        """Drop the database tables."""
        async with app.state.dishka_container(scope=Scope.REQUEST) as container:
            drop_database_tables = await container.get(DropDatabaseInteractor)
            await drop_database_tables()

    console.rule("Starting to drop the database")
    asyncio.run(_drop_database_tables())
    console.rule("Database dropped")


@click.command(
    help="Create all seed data for the application.",
)
@click.pass_obj
def seed_db(app: Litestar) -> None:
    """Create default seed data."""
    from rich import get_console

    # get the console
    console = get_console()

    async def _create_all_seed_data() -> None:
        """Create all seed data."""
        async with app.state.dishka_container(scope=Scope.REQUEST) as container:
            seed_database = await container.get(SeedDatabaseInteractor)
            await seed_database(
                request_model=SeedDatabaseRequestModel(
                    groups={
                        DatabaseSeedingGroups.subscriptions,
                        DatabaseSeedingGroups.users,
                    },
                ),
            )

    console.rule("Starting seed data creation")
    asyncio.run(_create_all_seed_data())
    console.rule("Stopping seed data creation")


core_controller.add_command(drop_db)
core_controller.add_command(seed_db)
