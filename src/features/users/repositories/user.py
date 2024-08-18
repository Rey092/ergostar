"""Repository for Subscriptions feature."""

from collections.abc import Sequence

from src.common.base.repositories.alchemy import AlchemyRepository
from src.common.base.repositories.alchemy import GenericAlchemyRepository
from src.features.users.entities.userentity import UserEntity
from src.features.users.models import UserModel


# noinspection DuplicatedCode
class UserRepository(AlchemyRepository[UserEntity, UserModel]):
    """Subscription Plan repository."""

    model_type = UserModel
    repository_type = GenericAlchemyRepository[UserModel]

    async def add_many(
        self,
        data: list[UserEntity],
    ) -> Sequence[UserEntity]:
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
