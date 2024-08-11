"""Interfaces for repositories in auth feature."""

from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.features.auth.entities.api_key import ApiKey
from src.features.users.entities.user import User


class ICreateApiKeyRepository(Protocol):
    """Interface for creating an API key."""

    @abstractmethod
    async def create_one(self, data: ApiKey) -> ApiKey:
        """Create an API key for user."""
        ...


class IGetUserByApiKeyRepository(Protocol):
    """Interface for getting user by API key."""

    @abstractmethod
    async def get_user_by_api_key_hash(self, api_key_hashed: str) -> User | None:
        """Get user by API key."""
        ...


class IGetAPIKeysRepository(Protocol):
    """Interface for getting API keys."""

    @abstractmethod
    async def get_api_keys(self, user_id: UUID) -> list[ApiKey]:
        """Get API keys for user."""
        ...
