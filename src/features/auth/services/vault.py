"""Vault service."""

from uuid import UUID

import hvac
import requests
from hvac.exceptions import InvalidPath
from litestar.concurrency import sync_to_thread

from src.common.base.service import Service
from src.config.settings import VaultSettings
from src.features.auth.entities.api_key import ApiKey
from src.features.auth.interfaces.repositories import IGetAPIKeysRepository
from src.features.auth.interfaces.services import IAddAPIKeyVaultService
from src.features.auth.interfaces.services import IGetAPIKeyListVaultService


class VaultService(
    Service,
    IGetAPIKeyListVaultService,
    IAddAPIKeyVaultService,
):
    """Vault service."""

    def __init__(
        self,
        vault_settings: VaultSettings,
        get_api_keys_repository: IGetAPIKeysRepository,
    ):
        """Initialize service."""
        self._vault_url: str = vault_settings.URL
        self._vault_token: str = vault_settings.TOKEN
        self._api_keys_mount_point = vault_settings.API_KEYS_MOUNT_POINT
        self._client = hvac.Client(
            session=requests.Session(),
            url=self._vault_url,
            token=self._vault_token,
            # TODO: add TLS
        )
        self._get_api_keys_repository = get_api_keys_repository

    async def get_api_key_list(self, user_id: UUID) -> list[ApiKey]:
        """Get secret."""
        # get data from vault
        data: dict[str, str] = await sync_to_thread(
            self._request_vault_api_keys_data,
            user_id=user_id,
        )

        # get api keys entities
        api_keys: list[ApiKey] = await self._get_api_keys_repository.get_api_keys(
            user_id=user_id,
        )

        # update api keys entities with the data from vault
        for api_key in api_keys:
            api_key_original_str: str | None = data.get(str(api_key.id), None)
            api_key.key_original = (
                UUID(api_key_original_str) if api_key_original_str else None
            )

        return api_keys

    def _request_vault_api_keys_data(self, user_id: UUID) -> dict[str, str]:
        """Get a user api key from vault.

        Key is the ApiKey ID and value is the ApiKey original value.
        """
        # get the secret data
        secret_version_response = self._client.secrets.kv.v2.read_secret_version(
            path=user_id,
            mount_point=self._api_keys_mount_point,
        )
        data: dict = secret_version_response["data"]["data"]

        # close the session
        self._client.session.close()

        return data

    async def add_api_key(self, user_id: UUID, api_key_id: str, api_key: str) -> None:
        """Add api key."""
        await sync_to_thread(
            self._request_add_api_key,
            user_id=user_id,
            api_key_id=api_key_id,
            api_key=api_key,
        )

    def _request_add_api_key(
        self,
        user_id: UUID,
        api_key_id: str,
        api_key: str,
    ) -> None:
        """Add api key."""
        # prepare data
        secret: dict[str, str] = {
            api_key_id: api_key,
        }

        try:
            # create a kv store
            self._client.sys.enable_secrets_engine(
                backend_type="kv",
                path=self._api_keys_mount_point,
            )
            # Try to read the existing data
            self._client.secrets.kv.v2.read_secret_version(
                path=user_id,
                mount_point=self._api_keys_mount_point,
            )
        except InvalidPath:
            # If the path does not exist, create it and add the secret
            self._client.secrets.kv.v2.create_or_update_secret(
                path=user_id,
                secret=secret,
                mount_point=self._api_keys_mount_point,
            )
        else:
            # If the path exists, update the secret
            self._client.secrets.kv.v2.patch(
                path=user_id,
                secret=secret,
                mount_point=self._api_keys_mount_point,
            )

        # close the session
        self._client.session.close()
