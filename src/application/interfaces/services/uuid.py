"""Core public interfaces."""

from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class IGenerateUUID7Service(Protocol):
    """Generate UUID7 service interface."""

    @abstractmethod
    def generate_uuid7(self) -> UUID:
        """Generate UUID7."""
        ...
