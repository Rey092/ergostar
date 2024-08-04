"""Create api key interactor."""

import logging
from dataclasses import dataclass

from src.common.base.use_case import UseCase
from src.common.interfaces.db import IDatabaseSession
from src.features.auth.entities.api_key import ApiKey
from src.features.auth.use_cases import interfaces

logger = logging.getLogger(__name__)


@dataclass
class CreateApiKeyRequestModel:
    """Create api key input data."""

    used_id: int


class CreateApiKeyUseCase(UseCase[CreateApiKeyRequestModel, None]):
    """Create api key use case."""

    def __init__(
        self,
        session: IDatabaseSession,
        create_api_key_repository: interfaces.ICreateApiKeyGateway,
    ):
        """Initialize interactor."""
        self._session = session
        self._create_api_key_repository = create_api_key_repository

    async def __call__(
        self,
        request_model: CreateApiKeyRequestModel,
        **kwargs,
    ) -> str:
        """Create an api key."""
        # create one
        api_key: ApiKey = await self._create_api_key_repository.create_one(
            ApiKey(
                user_id=request_model.used_id,
            ),
        )

        # commit
        await self._session.commit()

        return api_key.key
