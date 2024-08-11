"""This module contains the interfaces for the services of the auth feature."""

from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.features.auth.entities.api_key import ApiKey


class IGenerateUUID7Service(Protocol):
    """Generate UUID7 service interface."""

    @abstractmethod
    def generate_uuid7(self) -> str:
        """Generate UUID7."""
        ...


class IGetAPIKeyListVaultService(Protocol):
    """IGetAPIKeyList."""

    @abstractmethod
    async def get_api_key_list(self, user_id: UUID) -> list[ApiKey]:
        """Get api a key list."""
        ...


class IAddAPIKeyVaultService(Protocol):
    """IAddAPIKey."""

    @abstractmethod
    async def add_api_key(self, user_id: UUID, api_key_id: str, api_key: str) -> None:
        """Add api key."""
        ...
