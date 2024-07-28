"""User commands group."""

import click
from litestar import Litestar
from rich_click import RichContext

from .data import data
from .drop import drop


@click.group(
    name="seed",
    invoke_without_command=False,
    help="Create seed data for the application.",
)
@click.pass_context
def seed_group(context: RichContext, app: Litestar) -> None:
    """Manage application users."""
    context.obj = app


seed_group.add_command(data)  # type: ignore[no-untyped-call]
seed_group.add_command(drop)  # type: ignore[no-untyped-call]
