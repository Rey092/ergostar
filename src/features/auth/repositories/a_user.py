"""Auth user repository adapter."""

from sqlalchemy import select

from src.common.base.repositories.alchemy import AlchemyAdapterRepository
from src.common.base.repositories.alchemy import GenericSQLAlchemyRepository
from src.features.auth.interfaces.repositories import IGetUserByApiKeyRepository
from src.features.users import UserModel
from src.features.users.entities.userentity import UserEntity
from src.features.users.repositories.user import UserRepository


class AuthUserAdapterRepository(
    AlchemyAdapterRepository[UserEntity, UserModel, UserRepository],
    IGetUserByApiKeyRepository,
):
    """Auth user repository."""

    model_type = UserModel
    repository_type = GenericSQLAlchemyRepository[UserModel]

    async def get_user_by_api_key_hash(self, api_key_hashed: str) -> UserEntity | None:
        """Get user by API key."""
        model: UserModel | None = await self._repository.get_one_or_none(
            statement=select(UserModel)
            .join(UserModel.api_keys)
            .where(UserModel.api_keys.any(key_hashed=api_key_hashed))
            .distinct(),
        )
        return self.model_to_entity(model) if model else None
