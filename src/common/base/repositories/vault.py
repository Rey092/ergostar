"""Base repository class for Vault."""

from src.common.base.vault_uow import VaultSession


class VaultRepository:
    """Base repository class for Vault."""

    _session: VaultSession
