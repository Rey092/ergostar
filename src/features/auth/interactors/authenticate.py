"""AuthenticateApiKeyInteractor module."""

from dataclasses import dataclass

from litestar.exceptions import NotAuthorizedException

from src.common.base.interactor import Interactor
from src.features.auth.interfaces.hashers import IHasher
from src.features.auth.interfaces.repositories import IGetUserByApiKeyRepository
from src.features.auth.interfaces.services import IGenerateUUID7Service
from src.features.users.entities.userentity import UserEntity


@dataclass
class AuthenticateApiKeyRequestModel:
    """Authenticate an API key request model."""

    api_key: str


class AuthenticateApiKeyInteractor(
    Interactor[AuthenticateApiKeyRequestModel, UserEntity],
):
    """AuthenticateApiKeyInteractor."""

    def __init__(
        self,
        user_repository: IGetUserByApiKeyRepository,
        generate_uuid7_service: IGenerateUUID7Service,
        hash_service: IHasher,
    ):
        """Initialize interactor."""
        self._user_repository = user_repository
        self._generate_uuid7_service = generate_uuid7_service
        self._hash_service = hash_service

    async def __call__(
        self,
        request_model: AuthenticateApiKeyRequestModel,
        **kwargs,
    ) -> UserEntity:
        """Authenticate an API key."""
        # get api key hash
        api_key_hashed: str = self._hash_service.hash(request_model.api_key.encode())

        # get user by api key hash
        user: UserEntity | None = await self._user_repository.get_user_by_api_key_hash(
            api_key_hashed=api_key_hashed,
        )

        if not user:
            raise NotAuthorizedException

        return user
