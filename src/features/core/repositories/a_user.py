"""UserRepositoryAdapter."""

from collections.abc import Sequence

from src.common.base.repositories.alchemy import AlchemyAdapterRepository
from src.common.interfaces.fixture_loader.repository import ISeedRepository
from src.features.users.public.entities.user import UserEntity
from src.features.users.public.interfaces import IUserRepositoryContract


class UserRepositoryAdapter(
    AlchemyAdapterRepository[
        UserEntity,
        IUserRepositoryContract[UserEntity],
    ],
    ISeedRepository[UserEntity],
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
