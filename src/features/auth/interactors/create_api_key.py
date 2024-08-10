"""Create api key interactor."""

import logging
from dataclasses import dataclass

from src.common.base.interactor import UseCase
from src.common.interfaces.database_session import IAlchemySession
from src.features.auth.entities.api_key import ApiKey
from src.features.auth.interactors import interfaces

logger = logging.getLogger(__name__)


@dataclass
class CreateApiKeyRequestModel:
    """Create api key input data."""

    user_id: int


class CreateApiKeyInteractor(UseCase[CreateApiKeyRequestModel, str]):
    """Create api key use case."""

    def __init__(
        self,
        session: IAlchemySession,
        create_api_key_repository: interfaces.ICreateApiKeyRepository,
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
                user_id=request_model.user_id,
            ),
        )

        # commit
        await self._session.commit()

        return str(api_key.key)
