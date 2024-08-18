"""Interactor to get user api keys."""

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from hvac.exceptions import InvalidPath
from litestar.exceptions import ServiceUnavailableException

from src.common.base.interactor import Interactor
from src.features.auth.interfaces.repositories import IGetAPIKeysAlchemyRepository
from src.features.auth.interfaces.services import IGetAPIKeyListVaultRepository

if TYPE_CHECKING:
    from src.features.auth.entities.api_key import ApiKey


@dataclass
class GetUserApiKeysRequestModel:
    """Get user api keys request model."""

    user_id: UUID


class GetUserApiKeysInteractor(Interactor[GetUserApiKeysRequestModel, dict]):
    """Get user api keys."""

    def __init__(
        self,
        api_key_vault_repository: IGetAPIKeyListVaultRepository,
        api_key_alchemy_repository: IGetAPIKeysAlchemyRepository,
    ):
        """Configure the interactor."""
        self._api_key_vault_repository = api_key_vault_repository
        self._get_api_keys_repository = api_key_alchemy_repository

    async def __call__(self, request_model: GetUserApiKeysRequestModel) -> dict:
        """Get user api keys."""
        # get raw data from vault
        try:
            vault_api_keys: dict[
                str,
                str,
            ] = await self._api_key_vault_repository.get_user_api_keys(
                user_id=request_model.user_id,
            )
        except InvalidPath as error:
            raise ServiceUnavailableException from error

        # get api keys entities
        api_keys: list[ApiKey] = await self._get_api_keys_repository.get_api_keys(
            user_id=request_model.user_id,
        )

        # create a dict with keys: api_key_id, api_key_value,
        # date_created using api_keys and data
        api_keys_data: list[dict] = []

        for api_key in api_keys:
            vault_api_key_value: str | None = vault_api_keys.get(str(api_key.id), None)
            api_keys_data.append(
                {
                    "api_key_id": str(api_key.id),
                    "api_key_value": vault_api_key_value,
                    "date_created": api_key.created_at,
                },
            )

        return {
            "user_id": request_model.user_id,
            "api_keys": api_keys_data,
        }
