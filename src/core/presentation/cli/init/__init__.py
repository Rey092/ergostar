"""User commands group."""

import click
from litestar import Litestar
from rich_click import RichContext

from .landing import landing


@click.group(
    name="init",
    invoke_without_command=False,
    help="Create seed data for the application.",
)
@click.pass_context
def init_group(context: RichContext, app: Litestar) -> None:
    """Manage application users."""
    context.obj = app


# noinspection PyTypeChecker
init_group.add_command(landing)
