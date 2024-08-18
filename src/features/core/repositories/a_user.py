"""UserRepositoryAdapter."""

from collections.abc import Sequence

from src.common.base.repositories.alchemy import AlchemyAdapterRepository
from src.common.interfaces.fixture_loader.repository import ISeedManyEntries
from src.features.users import UserModel
from src.features.users.entities.userentity import UserEntity
from src.features.users.repositories.user import UserRepository


class UserRepositoryAdapter(
    AlchemyAdapterRepository[UserEntity, UserModel, UserRepository],
    ISeedManyEntries[UserEntity],
):
    """UserRepositoryAdapter."""

    async def add_many(
        self,
        data: list[UserEntity],
    ) -> Sequence[UserEntity]:
        """Add many entries."""
        return await self._adaptee.add_many(data)

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._adaptee.delete_everything()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._adaptee.exists_anything()
