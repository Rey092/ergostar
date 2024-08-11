"""Hasher using Blake-2b algorithm."""

import hashlib

from src.common.base.service import Service
from src.config.settings import AppSettings
from src.features.auth.interfaces.hashers import IHasher
from src.features.auth.interfaces.hashers import IHashVerifier


class HasherBlake2b(Service, IHasher, IHashVerifier):
    """Hasher using Blake algorithm."""

    def __init__(
        self,
        app_settings: AppSettings,
    ):
        """Initialize hasher."""
        self._key: bytes = app_settings.SECRET_KEY.encode()
        self._digest_size: int = app_settings.API_KEY_DIGEST_SIZE
        self._salt: bytes = b""

    def hash(self, data: bytes, person: bytes = b"") -> str:
        """Hash data."""
        return hashlib.blake2b(
            data,
            digest_size=self._digest_size,
            key=self._key,
            salt=self._salt,
            person=person,
        ).hexdigest()

    def verify(self, data: bytes, expected_hash: str, person: bytes = b"") -> bool:
        """Verify hash."""
        return self.hash(data, person) == expected_hash
