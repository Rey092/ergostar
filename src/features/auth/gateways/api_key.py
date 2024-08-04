"""Gateway for ApiKeys feature."""

from adaptix import P
from adaptix.conversion import get_converter
from adaptix.conversion import link_constant

from src.common.base.gateway import AlchemyGateway
from src.common.base.repository import GenericSQLAlchemyRepository
from src.common.interfaces.db import IDatabaseSession
from src.features.auth.entities.api_key import ApiKey
from src.features.auth.models import ApiKeyModel


class ApiKeyGateway(AlchemyGateway[ApiKeyModel]):
    """ApiKey gateway."""

    model_type = ApiKeyModel
    repository_type = GenericSQLAlchemyRepository[ApiKeyModel]

    def __init__(
        self,
        session: IDatabaseSession,
    ) -> None:
        """Initialize the gateway."""
        super().__init__(session)
        # TODO: Мне кажется собирать в __init__ конвертеры это плохая идея
        #  Жду фикса types в 'advanced-alchemy', до тех пор в класс конвертера не могу добавить
        #  И перенесу в аттрибуты класса или в декораторы
        #  Скорее всего в аттрибуты класса т.к. не нашёл кеширования в '@impl_converter'
        self.entity_to_model = get_converter(
            ApiKey,
            ApiKeyModel,
            recipe=[
                link_constant(P[ApiKeyModel].id, value=None),
            ],
        )
        self.model_to_entity = get_converter(
            ApiKeyModel,
            ApiKey,
        )

    async def create_one(self, data: ApiKey) -> ApiKey:
        """Delete all entries."""
        model = self.entity_to_model(data)
        await self._repository.add(model, auto_refresh=True)
        self.model_to_entity(model)
        return data
