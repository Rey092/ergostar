"""Gateway for Subscriptions feature."""

from collections.abc import Sequence

from sqlalchemy import select

from src.common.base.gateway import AlchemyGateway
from src.common.base.repository import GenericSQLAlchemyRepository
from src.features.users.entities import User
from src.features.users.models import UserModel


class UserGateway(AlchemyGateway[User, UserModel]):
    """Subscription Plan gateway."""

    model_type = UserModel
    repository_type = GenericSQLAlchemyRepository[UserModel]

    async def get_user_by_api_key(self, api_key: str) -> User | None:
        """Get user by api key."""
        model: UserModel | None = await self._repository.get_one_or_none(
            statement=select(UserModel)
            .join(UserModel.api_keys)
            .where(UserModel.api_keys.any(key=api_key))
            .distinct(),
        )
        return self.model_to_entity(model) if model else None

    async def add_many(
        self,
        data: list[User],
    ) -> Sequence[User]:
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
