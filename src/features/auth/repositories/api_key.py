"""Repository for ApiKeys feature."""

from src.common.base.repository import AlchemyRepository
from src.common.base.repository_generic import GenericSQLAlchemyRepository
from src.features.auth.entities.api_key import ApiKey
from src.features.auth.interactors.interfaces import ICreateApiKeyRepository
from src.features.auth.models import ApiKeyModel


class ApiKeyRepository(
    AlchemyRepository[ApiKey, ApiKeyModel],
    ICreateApiKeyRepository,
):
    """ApiKey repository."""

    model_type = ApiKeyModel
    repository_type = GenericSQLAlchemyRepository[ApiKeyModel]

    async def create_one(self, data: ApiKey) -> ApiKey:
        """Delete all entries."""
        model = self.entity_to_model(data)
        await self._repository.add(model, auto_refresh=True)
        return self.model_to_entity(model)
