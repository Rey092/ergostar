"""Interactor to get user api keys."""

from typing import TYPE_CHECKING
from uuid import UUID

from src.features.auth.interfaces.repositories import IGetAPIKeysAlchemyRepository
from src.features.auth.interfaces.services import IGetAPIKeyListVaultRepository

if TYPE_CHECKING:
    from src.features.auth.entities.api_key import ApiKey


class GetUserApiKeys:
    """Get user api keys."""

    def __init__(
        self,
        api_key_vault_repository: IGetAPIKeyListVaultRepository,
        api_key_alchemy_repository: IGetAPIKeysAlchemyRepository,
    ):
        """Configure the interactor."""
        self._api_key_vault_repository = api_key_vault_repository
        self._get_api_keys_repository = api_key_alchemy_repository

    async def __call__(self, user_id: UUID) -> dict[str, UUID | None]:
        """Get user api keys."""
        # get raw data from vault
        data: dict[str, str] = await self._api_key_vault_repository.get_user_api_keys(
            user_id=user_id,
        )

        # get api keys entities
        api_keys: list[ApiKey] = await self._get_api_keys_repository.get_api_keys(
            user_id=user_id,
        )

        # # update api keys entities with the data from vault
        for api_key in api_keys:
            api_key_original_str: str | None = data.get(str(api_key.id), None)
            api_key.key_original = (
                UUID(api_key_original_str) if api_key_original_str else None
            )

        return {str(api_key.id): api_key.key_original for api_key in api_keys}
