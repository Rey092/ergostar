"""User commands group."""

import click
from litestar import Litestar
from rich_click import RichContext

from .create_roles import create_roles


@click.group(
    name="users",
    invoke_without_command=False,
    help="Manage application users and roles.",
)
@click.pass_context
def users_group(context: RichContext, app: Litestar) -> None:
    """Manage application users."""
    context.obj = app


# noinspection PyTypeChecker
users_group.add_command(create_roles)
