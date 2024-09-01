"""AuthenticateApiKeyInteractor module."""

from dataclasses import dataclass

from litestar.exceptions import NotAuthorizedException

from src.application.common.interactor import Interactor
from src.application.interfaces.repositories.api_key import IGetUserByApiKeyRepository
from src.application.interfaces.services.hashers import IHasher
from src.application.interfaces.services.uuid import IGenerateUUID7Service
from src.domain.entities.users.user import User


@dataclass
class AuthenticateApiKeyRequestModel:
    """Authenticate an API key request model."""

    api_key: str


class AuthenticateApiKeyInteractor(
    Interactor[AuthenticateApiKeyRequestModel, User],
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
    ) -> User:
        """Authenticate an API key."""
        # get api key hash
        api_key_hashed: str = self._hash_service.hash(request_model.api_key.encode())

        # get user by api key hash
        user: User | None = await self._user_repository.get_user_by_api_key_hash(
            api_key_hashed=api_key_hashed,
        )

        if not user:
            raise NotAuthorizedException

        return user
