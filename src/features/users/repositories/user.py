"""Repository for Subscriptions feature."""

from collections.abc import Sequence

from src.common.base.repositories.alchemy import AlchemyRepository
from src.common.base.repositories.alchemy import GenericAlchemyRepository
from src.features.users.public.entities.user import UserEntity
from src.features.users.public.interfaces import IUserRepositoryContract


# noinspection DuplicatedCode
class UserRepository(
    AlchemyRepository[UserEntity],
    IUserRepositoryContract[UserEntity],
):
    """Subscription Plan repository."""

    entity_type = UserEntity
    repository_type = GenericAlchemyRepository[UserEntity]

    async def add_many(
        self,
        data: list[UserEntity],
    ) -> Sequence[UserEntity]:
        """Add many entries."""
        return await self._repository.add_many(data)

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._repository.delete_where()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._repository.exists()
