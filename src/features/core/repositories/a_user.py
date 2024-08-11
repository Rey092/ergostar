"""UserRepositoryAdapter."""

from collections.abc import Sequence

from src.common.interfaces.fixture_loader_repository import ISeedManyEntries
from src.features.users.entities.user import User
from src.features.users.repositories.user import UserRepository


class UserRepositoryAdapter(
    ISeedManyEntries[User],
):
    """UserRepositoryAdapter."""

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        """Initialize repository."""
        self._user_repository = user_repository

    async def add_many(
        self,
        data: list[User],
    ) -> Sequence[User]:
        """Add many entries."""
        return await self._user_repository.add_many(data)

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._user_repository.delete_everything()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._user_repository.exists_anything()
