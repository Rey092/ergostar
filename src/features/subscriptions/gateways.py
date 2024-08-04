"""Gateway for Subscriptions feature."""

from collections.abc import Sequence

from adaptix import P
from adaptix.conversion import get_converter
from adaptix.conversion import link_constant

from src.common.base.gateway import AlchemyGateway
from src.common.base.repository import GenericSQLAlchemyRepository
from src.common.interfaces.db import IDatabaseSession
from src.features.subscriptions import SubscriptionPlanModel
from src.features.subscriptions.entities import SubscriptionPlan


class SubscriptionPlanGateway(AlchemyGateway[SubscriptionPlanModel]):
    """Subscription Plan gateway."""

    model_type = SubscriptionPlanModel
    repository_type = GenericSQLAlchemyRepository[SubscriptionPlanModel]

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
            SubscriptionPlan,
            SubscriptionPlanModel,
            recipe=[
                link_constant(P[SubscriptionPlanModel].id, value=None),
            ],
        )
        self.model_to_entity = get_converter(
            SubscriptionPlanModel,
            SubscriptionPlan,
        )

    async def add_many(
        self,
        data: list[SubscriptionPlan],
    ) -> Sequence[SubscriptionPlan]:
        """Add many entries."""
        models = [self.entity_to_model(item) for item in data]
        entities = await self._repository.add_many(models)
        return [self.model_to_entity(item) for item in entities]

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._repository.delete_where()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._repository.exists()
