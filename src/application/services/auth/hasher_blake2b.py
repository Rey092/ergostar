"""Hasher using Blake-2b algorithm."""

import hashlib

from src.application.common.service import Service
from src.application.interfaces.services.hashers import IHasher
from src.application.interfaces.services.hashers import IHashVerifier
from src.main.config.settings import AppSettings


class HasherBlake2b(Service, IHasher, IHashVerifier):
    """Hasher using Blake-2b algorithm."""

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
