"""Cli commands for initializing the landing."""

import asyncio
import logging

import click
from dishka import AsyncContainer
from dishka import Scope
from litestar import Litestar

from src.features.core.interactors.seed_database import SeedDatabaseInteractor
from unfold.core.enums import DatabaseSeedingGroups

logger = logging.getLogger(__name__)


@click.command(
    help="Create all seed data for the application.",
)
@click.pass_obj
def data(app: Litestar) -> None:
    """Create default seed data."""
    from rich import get_console

    # get the console
    console = get_console()

    async def _create_all_seed_data() -> None:
        container: AsyncContainer = app.state.dishka_container
        async with container(scope=Scope.REQUEST) as container:
            seed_database = await container.get(SeedDatabaseInteractor)
            await seed_database(
                seeding_groups=[DatabaseSeedingGroups.landing],
            )

    console.rule("Starting seed data creation")
    asyncio.run(_create_all_seed_data())
    console.rule("Stopping seed data creation")
