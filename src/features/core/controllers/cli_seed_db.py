"""Cli commands for initializing the landing."""

import asyncio
import logging

import click
from dishka import Scope
from litestar import Litestar

from admin.core.enums import DatabaseSeedingGroups
from src.features.core.interactors.seed_database import SeedDatabaseRequestModel
from src.features.core.interactors.seed_database import SeedDatabaseUseCase

logger = logging.getLogger(__name__)


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
            seed_database = await container.get(SeedDatabaseUseCase)
            await seed_database(
                request_model=SeedDatabaseRequestModel(
                    groups=[DatabaseSeedingGroups.subscriptions],
                ),
            )

    console.rule("Starting seed data creation")
    asyncio.run(_create_all_seed_data())
    console.rule("Stopping seed data creation")
