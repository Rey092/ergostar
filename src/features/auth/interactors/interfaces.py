"""Interfaces for use cases in auth feature."""

from abc import abstractmethod
from typing import Protocol

from src.features.auth.entities.api_key import ApiKey


class ICreateApiKeyRepository(Protocol):
    """Interface for creating an API key."""

    @abstractmethod
    async def create_one(self, data: ApiKey) -> ApiKey:
        """Create an API key for user."""
        ...
