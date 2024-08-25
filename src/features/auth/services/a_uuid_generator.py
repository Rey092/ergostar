"""UUID generator service."""

from uuid import UUID

from src.common.base.service import Service
from src.features.auth.interfaces.services import IAuthGenerateUUID7Service
from src.features.core.public.interfaces import IGenerateUUID7Service


class AuthUUIDGeneratorAdapterService(
    Service,
    IAuthGenerateUUID7Service,
):
    """Generate UUID service."""

    def __init__(self, uuid_generator_service: IGenerateUUID7Service):
        """Initialize service."""
        self._adaptee = uuid_generator_service

    def generate_uuid7(self) -> UUID:
        """Generate UUID."""
        return self._adaptee.generate_uuid7()
