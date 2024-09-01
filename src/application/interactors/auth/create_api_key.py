"""Create api key interactor."""

import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.interactor import Interactor
from src.application.interfaces.repositories.api_key import ICreateApiKeyRepository
from src.application.interfaces.services.api_key import ICreateAPIKeyVaultRepository
from src.application.interfaces.services.hashers import IHasher
from src.application.interfaces.services.uuid import IGenerateUUID7Service
from src.domain.entities.auth.api_key import ApiKey
from src.infrastructure.interfaces.uow import IDatabaseSession
from src.infrastructure.interfaces.uow import IVaultSession

logger = logging.getLogger(__name__)


@dataclass
class CreateApiKeyRequestModel:
    """Create api key input data."""

    user_id: UUID


class CreateApiKeyInteractor(Interactor[CreateApiKeyRequestModel, UUID]):
    """Create api key interactor."""

    def __init__(
        self,
        db_session: IDatabaseSession,
        vault_session: IVaultSession,
        create_api_key_repository: ICreateApiKeyRepository,
        uuid7_generator_service: IGenerateUUID7Service,
        hasher_service: IHasher,
        vault_repository: ICreateAPIKeyVaultRepository,
    ):
        """Initialize interactor."""
        self._db_session = db_session
        self._vault_session = vault_session
        self._create_api_key_repository = create_api_key_repository
        self._uuid7_generator_service = uuid7_generator_service
        self._hasher_service = hasher_service
        self._vault_service = vault_repository

    async def __call__(
        self,
        request_model: CreateApiKeyRequestModel,
    ) -> UUID:
        """Create an api key."""
        # TODO: limit API keys to N per user.
        #  prevent race condition with rate limit or FOR UPDATE

        # generate UUID7 key
        api_key_value: UUID = self._uuid7_generator_service.generate_uuid7()

        # hash key
        key_hashed: str = self._hasher_service.hash(str(api_key_value).encode())

        # create one
        api_key: ApiKey = await self._create_api_key_repository.create_one(
            ApiKey(
                user_id=request_model.user_id,
                key_hashed=key_hashed,
            ),
        )

        # add to vault
        await self._vault_service.add_api_key(
            user_id=request_model.user_id,
            api_key_id=str(api_key.id),
            api_key=api_key_value,
        )

        # save changes
        await self._vault_session.flush()
        await self._db_session.commit()
        await self._vault_session.commit()

        return api_key_value
