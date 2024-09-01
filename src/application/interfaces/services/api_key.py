"""This module contains the interfaces for the services of the auth feature."""

from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class IGetAPIKeysVaultRepository(Protocol):
    """IGetAPIKeyList."""

    @abstractmethod
    async def get_user_api_keys(self, user_id: UUID) -> dict[str, str]:
        """Get api a key list."""
        ...


class ICreateAPIKeyVaultRepository(Protocol):
    """IAddAPIKey."""

    @abstractmethod
    async def add_api_key(self, user_id: UUID, api_key_id: str, api_key: UUID) -> None:
        """Add api key."""
        ...
