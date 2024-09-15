"""Base repository class for Vault."""

from src.infrastructure.vault.session import VaultSession


class VaultRepository:
    """Base repository class for Vault."""

    _session: VaultSession
    _mount_point: str

    def __init__(self, session: VaultSession):
        """Initialize repository."""
        self._session = session
