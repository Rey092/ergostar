"""Interfaces for hashers."""

from abc import abstractmethod
from typing import Protocol


class IHasher(Protocol):
    """Hasher interface."""

    @abstractmethod
    def hash(
        self,
        data: bytes,
    ) -> str:
        """Hash data."""


class IHashVerifier(Protocol):
    """Hash verifier interface."""

    @abstractmethod
    def verify(
        self,
        data: bytes,
        expected_hash: str,
    ) -> bool:
        """Verify hash."""
