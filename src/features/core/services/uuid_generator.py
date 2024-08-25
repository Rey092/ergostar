"""UUID generator service."""

from uuid import UUID

from uuid_utils import uuid7

from src.common.base.service import Service
from src.features.core.public.interfaces import IGenerateUUID7Service


class UUIDGeneratorService(
    Service,
    IGenerateUUID7Service,
):
    """Generate UUID service."""

    def generate_uuid7(self) -> UUID:
        """Generate UUID."""
        return UUID(str(uuid7()))
