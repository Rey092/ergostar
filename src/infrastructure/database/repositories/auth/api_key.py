"""Repository for ApiKeys feature."""

from uuid import UUID

from src.application.interfaces.repositories.api_key import ICreateApiKeyRepository
from src.application.interfaces.repositories.api_key import IGetAPIKeysAlchemyRepository
from src.domain.entities.auth.api_key import ApiKey
from src.infrastructure.database.base import AlchemyRepository
from src.infrastructure.database.base import GenericAlchemyRepository


class ApiKeyRepository(
    AlchemyRepository[ApiKey],
    ICreateApiKeyRepository,
    IGetAPIKeysAlchemyRepository,
):
    """ApiKey repository."""

    entity_type = ApiKey
    repository_type = GenericAlchemyRepository[ApiKey]

    async def create_one(self, data: ApiKey) -> ApiKey:
        """Delete all entries."""
        return await self._repository.add(data, auto_refresh=True)

    async def get_api_keys(self, user_id: UUID) -> list[ApiKey]:
        """Get API keys for user."""
        return await self._repository.list(user_id=user_id)
