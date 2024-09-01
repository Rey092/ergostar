"""Repository for Subscriptions feature."""

from collections.abc import Sequence

from sqlalchemy import select

from src.application.interfaces.repositories.api_key import IGetUserByApiKeyRepository
from src.application.interfaces.repositories.seed import ISeedRepository
from src.domain.entities.users.user import User
from src.infrastructure.database.base import AlchemyRepository
from src.infrastructure.database.base import GenericAlchemyRepository
from src.infrastructure.database.tables import api_key_table


class UserRepository(
    AlchemyRepository[User],
    IGetUserByApiKeyRepository,
    ISeedRepository[User],
):
    """Subscription Plan repository."""

    entity_type = User
    repository_type = GenericAlchemyRepository[User]

    async def add_many(
        self,
        data: list[User],
    ) -> Sequence[User]:
        """Add many entries."""
        return await self._repository.add_many(data)

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._repository.delete_where()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._repository.exists()

    # TODO: https://youtrack.jetbrains.com/issue/PY-71748/SQLAlchemy-2.0-ORM-filter-show-wrong-type-hints-in-Pycharm
    # noinspection PyTypeChecker
    async def get_user_by_api_key_hash(self, api_key_hashed: str) -> User | None:
        """Get user by API key."""
        user: User | None = await self._repository.get_one_or_none(
            statement=select(User)
            .join(api_key_table)
            .where(
                api_key_table.c.key_hashed == api_key_hashed,
            ),
        )
        return user
