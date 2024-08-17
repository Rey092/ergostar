"""Vault Unit of Work."""

import logging
import types
from collections.abc import Callable
from typing import Any

from hvac import Client as VaultEngine
from hvac.exceptions import InvalidPath
from litestar.concurrency import sync_to_thread
from requests import Session

from src.common.interfaces.unit_of_work import IVaultSession

logger = logging.getLogger(__name__)


class VaultOperation:
    """Encapsulates a Vault operation and its corresponding rollback."""

    def __init__(
        self,
        execute: Callable[[], Any],
        rollback: Callable[[], Any] | None = None,
    ):
        """Initialize the operation."""
        self.execute = execute
        self.rollback = rollback
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


class VaultSession(IVaultSession):
    """Vault Unit of Work."""

    rolling_back_message = "Vault operations failed, rolling back: %s"
    rollback_failed_message = "Rollback failed: %s"

    def __init__(self, vault_engine: VaultEngine):
        """Initialize the Vault session."""
        self.vault_engine = vault_engine
        self._operations: list[VaultOperation] = []
        self._committed = False

    async def __aenter__(self) -> "VaultSession":
        """Enter the context manager."""
        self._clear()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        """Exit the context manager."""
        if exc_type:
            await self.rollback()
        await self.close()

    def begin(self) -> "VaultSessionContextManager":
        """Begin a new transaction."""
        return VaultSessionContextManager(self)

    def _clear(self) -> None:
        """Clear all operations."""
        self._operations.clear()
        self._committed = False

    async def close(self) -> None:
        """Close the Vault session."""
        if not self._committed:
            await self.rollback()
        self._clear()

    def add_operation(
        self,
        execute: Callable[[], Any],
        rollback: Callable[[], Any] | None = None,
    ) -> None:
        """Add an operation and its rollback to the unit of work."""
        self._operations.append(VaultOperation(execute, rollback))

    async def commit(self) -> None:
        """Commit all operations."""
        logger.info("Committing Vault operations")
        try:
            await self.flush()
            self._clear()
            self._committed = True
            logger.info("Vault operations committed")
        except Exception as error:
            logger.info(self.rolling_back_message, error)
            await self.rollback()
            raise

    async def rollback(self) -> None:
        """Rollback all operations in reverse order."""
        for operation in reversed(self._operations):
            try:
                await operation.undo()
            except Exception as error:  # noqa: BLE001
                logger.warning(self.rollback_failed_message, error)

    async def flush(self) -> None:
        """Execute all operations without committing."""
        for operation in self._operations:
            await operation.run()

    def create_or_patch(
        self,
        path: str,
        key: str,
        value: str,
        mount_point: str = "",
    ) -> None:
        """Add an operation to create or update a key in the Vault."""

        async def execute():
            """Execute the operation."""
            try:
                # try to patch the secret
                await sync_to_thread(
                    self.vault_engine.secrets.kv.v2.patch,
                    path=path,
                    secret={key: value},
                    mount_point=mount_point,
                )
            except InvalidPath:
                # if the secret does not exist, create it
                await sync_to_thread(
                    self.vault_engine.secrets.kv.v2.create_or_update_secret,
                    path,
                    {key: value},
                    mount_point=mount_point,
                )

        async def rollback():
            """Rollback the operation."""
            try:
                response = await sync_to_thread(
                    self.vault_engine.secrets.kv.v2.read_secret,
                    path=path,
                    mount_point=mount_point,
                )
                current_data = response["data"]["data"]
            except InvalidPath:
                return
            if key in current_data:
                del current_data[key]
                await sync_to_thread(
                    self.vault_engine.secrets.kv.v2.create_or_update_secret,
                    path=path,
                    secret=current_data,
                    mount_point=mount_point,
                )

        self.add_operation(execute, rollback)

    async def read_secret(self, path: str, mount_point: str = "") -> dict:
        """Add an operation to read a secret from the Vault."""
        response = await sync_to_thread(
            self.vault_engine.secrets.kv.v2.read_secret,
            path=path,
            mount_point=mount_point,
        )
        return response["data"]["data"]


class VaultSessionContextManager:
    """Vault Unit of Work context manager."""

    __slots__ = ("vault_session",)

    def __init__(self, vault_session: VaultSession):
        """Initialize the context manager."""
        self.vault_session = vault_session

    async def __aenter__(self) -> VaultSession:
        """Enter the context manager."""
        await self.vault_session.__aenter__()
        self.vault_session.vault_engine.session = Session()
        return self.vault_session

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        """Exit the context manager."""
        await self.vault_session.__aexit__(exc_type, exc_value, traceback)
        await self.vault_session.close()
        self.vault_session.vault_engine.session.close()
