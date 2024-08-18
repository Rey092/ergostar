"""Interactor to get user api keys."""

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from litestar.exceptions import ClientException

from src.common.base.interactor import Interactor
from src.features.auth.interfaces.repositories import IGetAPIKeysAlchemyRepository
from src.features.auth.interfaces.services import IGetAPIKeyListVaultRepository

if TYPE_CHECKING:
    from src.features.auth.entities.api_key import ApiKeyEntity


@dataclass
class GetUserApiKeysRequestModel:
    """Get user api keys request model."""

    user_id: UUID


@dataclass
class UserApiKey:
    """User api key."""

    api_key_id: str
    api_key_value: str | None
    date_created: datetime
    useless_field_two: str


@dataclass
class GetUserApiKeysResponseModel:
    """Get user api keys response model."""

    user_id: UUID
    api_keys: list[UserApiKey]
    useless_field_one: str = "This field should be hidden."


class GetUserApiKeysInteractor(
    Interactor[GetUserApiKeysRequestModel, GetUserApiKeysResponseModel],
):
    """Get user api keys."""

    def __init__(
        self,
        api_key_vault_repository: IGetAPIKeyListVaultRepository,
        api_key_alchemy_repository: IGetAPIKeysAlchemyRepository,
    ):
        """Configure the interactor."""
        self._api_key_vault_repository = api_key_vault_repository
        self._get_api_keys_repository = api_key_alchemy_repository
        self._message_create_api_key_first = (
            "Before you can use this feature, you need to create an API key first."
        )

    async def __call__(
        self,
        request_model: GetUserApiKeysRequestModel,
    ) -> GetUserApiKeysResponseModel:
        """Get user api keys."""
        # get api keys entities
        api_keys: list[ApiKeyEntity] = await self._get_api_keys_repository.get_api_keys(
            user_id=request_model.user_id,
        )

        # if no api keys found raise exception
        if not api_keys:
            raise ClientException(
                detail=self._message_create_api_key_first,
            )

        # get raw data from vault
        vault_api_keys: dict[
            str,
            str,
        ] = await self._api_key_vault_repository.get_user_api_keys(
            user_id=request_model.user_id,
        )

        # create a dict with keys: api_key_id, api_key_value,
        # date_created using api_keys and data
        api_keys_data: list[UserApiKey] = []

        for api_key in api_keys:
            vault_api_key_value: str | None = vault_api_keys.get(str(api_key.id), None)
            api_keys_data.append(
                UserApiKey(
                    api_key_id=str(api_key.id),
                    api_key_value=vault_api_key_value,
                    date_created=api_key.created_at,
                    useless_field_two="This field should be hidden.",
                ),
            )

        return GetUserApiKeysResponseModel(
            user_id=request_model.user_id,
            api_keys=api_keys_data,
        )
