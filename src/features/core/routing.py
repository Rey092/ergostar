"""Health router module."""

import click
from litestar import Litestar
from litestar import Router
from rich_click import RichContext

from src.features.core.controllers.api_health import HealthController
from src.features.core.controllers.cli_drop_db import drop_db
from src.features.core.controllers.cli_seed_db import seed_db

health_router = Router(
    path="/health",
    route_handlers=[HealthController],
    include_in_schema=False,
)


@click.group(
    name="seed",
    invoke_without_command=False,
    help="Core methods for the application. Database seeding, dropping, etc.",
)
@click.pass_context
def core_group(context: RichContext, app: Litestar) -> None:
    """Manage application users."""
    context.obj = app


# noinspection PyTypeChecker
core_group.add_command(seed_db)
# noinspection PyTypeChecker
core_group.add_command(drop_db)
