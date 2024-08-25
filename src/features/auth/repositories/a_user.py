"""Auth user repository adapter."""

from sqlalchemy import select

from src.common.base.repositories.alchemy import AlchemyRepository
from src.common.base.repositories.alchemy import GenericAlchemyRepository
from src.features.auth.interfaces.repositories import IGetUserByApiKeyRepository
from src.features.auth.public.tables import ApiKeyTable
from src.features.users.public.entities.user import UserEntity


class AuthUserRepository(
    AlchemyRepository[UserEntity],
    IGetUserByApiKeyRepository,
):
    """Auth user repository."""

    entity_type = UserEntity
    repository_type = GenericAlchemyRepository[UserEntity]

    # TODO: https://youtrack.jetbrains.com/issue/PY-71748/SQLAlchemy-2.0-ORM-filter-show-wrong-type-hints-in-Pycharm
    # noinspection PyTypeChecker
    async def get_user_by_api_key_hash(self, api_key_hashed: str) -> UserEntity | None:
        """Get user by API key."""
        user: UserEntity | None = await self._repository.get_one_or_none(
            statement=select(UserEntity)
            .join(ApiKeyTable)
            .where(
                ApiKeyTable.c.key_hashed == api_key_hashed,
            ),
        )
        return user
