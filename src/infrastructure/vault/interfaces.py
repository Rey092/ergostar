"""Base repository class for Vault."""

from src.infrastructure.vault.base import VaultSession


class VaultRepository:
    """Base repository class for Vault."""

    _session: VaultSession
