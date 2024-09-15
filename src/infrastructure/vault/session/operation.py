"""Encapsulates a Vault operation and its corresponding rollback."""

from collections.abc import Callable
from typing import Any


class VaultOperation:
    """Encapsulates a Vault operation and its corresponding rollback."""

    def __init__(
        self,
        execute: Callable[[], Any],
        rollback: Callable[[], Any] | None = None,
        mount_point: str = "secret",
    ):
        """Initialize the operation.

        Args:
            execute: The operation to execute.
            rollback: The operation to roll back the execute operation.
            mount_point: The Vault mount point to use.
        """
        self.execute = execute
        self.rollback = rollback
        self.mount_point = mount_point
        self.is_executed = False
        self.is_rolled_back = False

    async def run(self):
        """Run the operation."""
        if not self.is_executed:
            await self.execute()
            self.is_executed = True

    async def undo(self):
        """Run the rollback operation, if provided."""
        if self.rollback and self.is_executed and not self.is_rolled_back:
            await self.rollback()
            self.is_rolled_back = True
