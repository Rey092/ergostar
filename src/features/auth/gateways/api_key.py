"""Gateway for ApiKeys feature."""

from src.common.base.gateway import AlchemyGateway
from src.common.base.repository import GenericSQLAlchemyRepository
from src.features.auth.entities.api_key import ApiKey
from src.features.auth.models import ApiKeyModel
from src.features.auth.use_cases.interfaces import ICreateApiKeyGateway


class ApiKeyGateway(
    AlchemyGateway[ApiKey, ApiKeyModel],
    ICreateApiKeyGateway,
):
    """ApiKey gateway."""

    model_type = ApiKeyModel
    repository_type = GenericSQLAlchemyRepository[ApiKeyModel]

    async def create_one(self, data: ApiKey) -> ApiKey:
        """Delete all entries."""
        model = self.entity_to_model(data)
        await self._repository.add(model, auto_refresh=True)
        return self.model_to_entity(model)
