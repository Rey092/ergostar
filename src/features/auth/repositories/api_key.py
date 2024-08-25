"""Repository for ApiKeys feature."""

from uuid import UUID

from src.common.base.repositories.alchemy import AlchemyRepository
from src.common.base.repositories.alchemy import GenericAlchemyRepository
from src.features.auth.entities.api_key import ApiKeyEntity
from src.features.auth.interfaces.repositories import ICreateApiKeyRepository
from src.features.auth.interfaces.repositories import IGetAPIKeysAlchemyRepository


class ApiKeyRepository(
    AlchemyRepository[ApiKeyEntity],
    ICreateApiKeyRepository,
    IGetAPIKeysAlchemyRepository,
):
    """ApiKey repository."""

    entity_type = ApiKeyEntity
    repository_type = GenericAlchemyRepository[ApiKeyEntity]

    async def create_one(self, data: ApiKeyEntity) -> ApiKeyEntity:
        """Delete all entries."""
        return await self._repository.add(data, auto_refresh=True)

    async def get_api_keys(self, user_id: UUID) -> list[ApiKeyEntity]:
        """Get API keys for user."""
        return await self._repository.list(user_id=user_id)
