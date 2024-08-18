"""Repository for ApiKeys feature."""

from uuid import UUID

from src.common.base.repositories.alchemy import AlchemyMappedRepository
from src.common.base.repositories.alchemy import GenericSQLAlchemyRepository
from src.features.auth.entities.api_key import ApiKeyEntity
from src.features.auth.interfaces.repositories import ICreateApiKeyRepository
from src.features.auth.interfaces.repositories import IGetAPIKeysAlchemyRepository
from src.features.auth.models import ApiKeyModel


class ApiKeyRepository(
    AlchemyMappedRepository[ApiKeyEntity, ApiKeyModel],
    ICreateApiKeyRepository,
    IGetAPIKeysAlchemyRepository,
):
    """ApiKey repository."""

    model_type = ApiKeyModel
    repository_type = GenericSQLAlchemyRepository[ApiKeyModel]

    async def create_one(self, data: ApiKeyEntity) -> ApiKeyEntity:
        """Delete all entries."""
        model = self.entity_to_model(data)
        await self._repository.add(model, auto_refresh=True)
        return self.model_to_entity(model)

    async def get_api_keys(self, user_id: UUID) -> list[ApiKeyEntity]:
        """Get API keys for user."""
        models = await self._repository.list(user_id=user_id)
        return [self.model_to_entity(model) for model in models]
