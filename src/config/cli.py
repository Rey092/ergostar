"""Application configuration plugin."""

from click import Group
from litestar.plugins import CLIPluginProtocol


class CLIPlugin(CLIPluginProtocol):
    """CLI plugin."""

    # noinspection PyTypeChecker
    def on_cli_init(self, cli: Group) -> None:
        """Add commands to the CLI."""
        from src.features.core.routing import core_group

        cli.add_command(core_group)
