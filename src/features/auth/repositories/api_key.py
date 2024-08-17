"""Repository for ApiKeys feature."""

from uuid import UUID

from src.common.base.basealchemyrepository import AlchemyMappedRepository
from src.common.base.repository_generic import GenericSQLAlchemyRepository
from src.features.auth.entities.api_key import ApiKey
from src.features.auth.interfaces.repositories import ICreateApiKeyRepository
from src.features.auth.interfaces.repositories import IGetAPIKeysAlchemyRepository
from src.features.auth.models import ApiKeyModel


class ApiKeyRepository(
    AlchemyMappedRepository[ApiKey, ApiKeyModel],
    ICreateApiKeyRepository,
    IGetAPIKeysAlchemyRepository,
):
    """ApiKey repository."""

    model_type = ApiKeyModel
    repository_type = GenericSQLAlchemyRepository[ApiKeyModel]

    async def create_one(self, data: ApiKey) -> ApiKey:
        """Delete all entries."""
        model = self.entity_to_model(data)
        await self._repository.add(model, auto_refresh=True)
        return self.model_to_entity(model)

    async def get_api_keys(self, user_id: UUID) -> list[ApiKey]:
        """Get API keys for user."""
        models = await self._repository.list(user_id=user_id)
        return [self.model_to_entity(model) for model in models]
