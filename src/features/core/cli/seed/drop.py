"""Drop all data."""
import asyncio

import click
from dishka import AsyncContainer, Scope
from litestar import Litestar
from src.features.core.interactors.drop_database import DropDatabaseInteractor


@click.command(
    help="Drop all data in the database.",
)
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
@click.pass_obj
def drop(app: Litestar) -> None:
    """Drop all data in the database."""
    import anyio
    from rich import get_console

    # get the console
    console = get_console()

    async def _drop_database() -> None:
        console.rule("Loading landing data")
        container: AsyncContainer = app.state.dishka_container
        async with container(scope=Scope.REQUEST) as container:
            drop_database = await container.get(DropDatabaseInteractor)
            await drop_database()

    console.rule("Starting to drop the database")
    asyncio.run(_drop_database())
    console.rule("Database dropped")
