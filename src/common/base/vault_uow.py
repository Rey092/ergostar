"""Vault Unit of Work module."""
from hvac import Client
from litestar.concurrency import sync_to_thread


class VaultUnitOfWork:
    """Vault Unit of Work."""

    def __init__(self, vault_client: Client):
        """Initialize the unit of work."""
        self.vault_client = vault_client
        self._operations = []
        self._rollback_operations = []

    async def __aenter__(self):
        """Enter the context manager."""
        self.begin()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Exit the context manager."""
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    def begin(self):
        """Begin a new unit of work."""
        self._operations.clear()
        self._rollback_operations.clear()

    def add_operation(self, operation, rollback_operation=None):
        """Add an operation to the unit of work."""
        self._operations.append(operation)
        if rollback_operation:
            self._rollback_operations.append(rollback_operation)

    async def commit(self):
        """Commit all operations."""
        try:
            await self.flush()  # Flush operations before finalizing
            self._operations.clear()
            self._rollback_operations.clear()
        except Exception as e:
            await self.rollback()
            raise e

    async def rollback(self):
        for rollback_operation in reversed(self._rollback_operations):
            try:
                await sync_to_thread(rollback_operation)
            except Exception as e:
                # Handle rollback failure if necessary
                pass

    async def flush(self):
        """
        Execute all operations without committing.
        This is useful if you want to apply changes incrementally or validate state.
        """
        for operation in self._operations:
            await sync_to_thread(operation)

    async def add(self, path, key, value):
        """
        Adds an operation to add or update a key in the Vault at the specified path.
        If the path exists, it patches the existing data; if not, it creates the path with the key.
        """

        async def operation():
            """Add or update a key in the Vault at the specified path."""
            # Check if path exists
            path_exists = await sync_to_thread(
                lambda: self.vault_client.secrets.kv.v2.read_metadata(path)
            )
            if path_exists:
                # Path exists, patch it with a new key
                await sync_to_thread(
                    lambda: self.vault_client.secrets.kv.v2.patch(path, {key: value})
                )
            else:
                # Path does not exist, create it with the key
                await sync_to_thread(
                    lambda: self.vault_client.secrets.kv.v2.create_or_update_secret(path, {key: value})
                )

        async def rollback_operation():
            """Rollback logic to remove the key if it was added."""
            # Rollback logic to remove the key if it was added
            current_data = await sync_to_thread(
                lambda: self.vault_client.secrets.kv.v2.read_secret(path)['data']['data']
            )
            if key in current_data:
                del current_data[key]
                await sync_to_thread(
                    lambda: self.vault_client.secrets.kv.v2.create_or_update_secret(path, current_data)
                )

        self.add_operation(operation, rollback_operation)
