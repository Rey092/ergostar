"""Vault service."""

from uuid import UUID

from src.common.base.repositories.vault import VaultRepository
from src.common.base.vault_uow import VaultSession
from src.config.settings import VaultSettings
from src.features.auth.interfaces.services import IAddAPIKeyVaultRepository
from src.features.auth.interfaces.services import IGetAPIKeyListVaultRepository


class ApiKeyVaultRepository(
    VaultRepository,
    IGetAPIKeyListVaultRepository,
    IAddAPIKeyVaultRepository,
):
    """Vault service."""

    def __init__(
        self,
        session: VaultSession,
        vault_settings: VaultSettings,
    ):
        """Initialize service."""
        self._session = session
        self._mount_point = vault_settings.API_KEYS_MOUNT_POINT

    async def get_user_api_keys(self, user_id: UUID) -> dict[str, str]:
        """Get user api keys as a dictionary.

        Key is the api key id stored in the database.
        Value is the real api key value.
        """
        data: dict[str, str] = await self._session.read_secret(
            path=str(user_id),
            mount_point=self._mount_point,
        )

        return data

    async def add_api_key(self, user_id: UUID, api_key_id: str, api_key: UUID) -> None:
        """Add api key."""
        self._session.create_or_patch(
            path=str(user_id),
            key=api_key_id,
            value=str(api_key),
            mount_point=self._mount_point,
        )
