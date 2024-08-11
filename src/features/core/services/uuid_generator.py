"""UUID generator service."""

from uuid_utils import uuid7

from src.common.base.service import Service


class UUIDGeneratorService(Service):
    """Generate UUID service."""

    @staticmethod
    def generate_uuid7() -> str:
        """Generate UUID."""
        return str(uuid7())
