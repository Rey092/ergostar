"""Create api key interactor."""

import logging
import uuid
from dataclasses import dataclass

from src.common.base.interactor import Interactor
from src.common.interfaces.uow import IDatabaseSession
from src.common.interfaces.uow import IVaultSession
from src.features.auth.entities.api_key import ApiKeyEntity
from src.features.auth.interfaces.hashers import IHasher
from src.features.auth.interfaces.repositories import ICreateApiKeyRepository
from src.features.auth.interfaces.services import IAddAPIKeyVaultRepository
from src.features.auth.interfaces.services import IGenerateUUID7Service

logger = logging.getLogger(__name__)


@dataclass
class CreateApiKeyRequestModel:
    """Create api key input data."""

    user_id: uuid.UUID


class CreateApiKeyInteractor(Interactor[CreateApiKeyRequestModel, str]):
    """Create api key interactor."""

    def __init__(
        self,
        db_session: IDatabaseSession,
        vault_session: IVaultSession,
        create_api_key_repository: ICreateApiKeyRepository,
        uuid7_generator_service: IGenerateUUID7Service,
        hasher_service: IHasher,
        vault_repository: IAddAPIKeyVaultRepository,
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
        **kwargs,
    ) -> str:
        """Create an api key."""
        # generate UUID7 key
        key: str = self._uuid7_generator_service.generate_uuid7()

        # hash key
        key_hashed: str = self._hasher_service.hash(key.encode())

        # create one
        api_key: ApiKeyEntity = await self._create_api_key_repository.create_one(
            ApiKeyEntity(
                user_id=request_model.user_id,
                key_hashed=key_hashed,
            ),
        )

        # add to vault
        await self._vault_service.add_api_key(
            user_id=request_model.user_id,
            api_key_id=str(api_key.id),
            api_key=key,
        )

        # save changes
        await self._vault_session.flush()
        await self._db_session.commit()
        await self._vault_session.commit()

        return key
