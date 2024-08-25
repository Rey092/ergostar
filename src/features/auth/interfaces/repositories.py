"""Interfaces for repositories in auth feature."""

from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.features.auth.entities.api_key import ApiKeyEntity
from src.features.users.public.entities.user import UserEntity


class ICreateApiKeyRepository(Protocol):
    """Interface for creating an API key."""

    @abstractmethod
    async def create_one(self, data: ApiKeyEntity) -> ApiKeyEntity:
        """Create an API key for user."""
        ...


class IGetUserByApiKeyRepository(Protocol):
    """Interface for getting user by API key."""

    @abstractmethod
    async def get_user_by_api_key_hash(self, api_key_hashed: str) -> UserEntity | None:
        """Get user by API key."""
        ...


class IGetAPIKeysAlchemyRepository(Protocol):
    """Interface for getting API keys."""

    @abstractmethod
    async def get_api_keys(self, user_id: UUID) -> list[ApiKeyEntity]:
        """Get API keys for user."""
        ...
