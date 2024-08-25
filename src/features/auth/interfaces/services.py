"""This module contains the interfaces for the services of the auth feature."""

from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class IAuthGenerateUUID7Service(Protocol):
    """Generate UUID7 service interface."""

    @abstractmethod
    def generate_uuid7(self) -> UUID:
        """Generate UUID7."""
        ...


class IGetAPIKeyListVaultRepository(Protocol):
    """IGetAPIKeyList."""

    @abstractmethod
    async def get_user_api_keys(self, user_id: UUID) -> dict[str, str]:
        """Get api a key list."""
        ...


class IAddAPIKeyVaultRepository(Protocol):
    """IAddAPIKey."""

    @abstractmethod
    async def add_api_key(self, user_id: UUID, api_key_id: str, api_key: UUID) -> None:
        """Add api key."""
        ...
