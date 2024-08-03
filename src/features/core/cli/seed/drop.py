"""Drop all data."""

import asyncio

import click
from dishka import AsyncContainer
from dishka import Scope
from litestar import Litestar

from src.features.core.use_cases.drop_database import DropDatabaseTablesUseCase


@click.command(
    help="Drop all data in the database.",
)
@click.confirmation_option(prompt="Are you sure you want to drop the db?")
@click.pass_obj
def drop(app: Litestar) -> None:
    """Drop all data in the database."""
    from rich import get_console

    # get the console
    console = get_console()

    async def _drop_database() -> None:
        console.rule("Loading landing data")
        container: AsyncContainer = app.state.dishka_container
        async with container(scope=Scope.REQUEST) as container:
            drop_database_tables = await container.get(DropDatabaseTablesUseCase)
            await drop_database_tables()

    console.rule("Starting to drop the database")
    asyncio.run(_drop_database())
    console.rule("Database dropped")
