"""UUID generator service."""

from src.common.base.service import Service
from src.features.auth.interfaces.services import IGenerateUUID7Service
from src.features.core.services.uuid_generator import UUIDGeneratorService


class AuthUUIDGeneratorAdapterService(
    Service,
    IGenerateUUID7Service,
):
    """Generate UUID service."""

    def __init__(self, uuid_generator_service: UUIDGeneratorService):
        """Initialize service."""
        self._uuid_generator_service = uuid_generator_service

    def generate_uuid7(self) -> str:
        """Generate UUID."""
        return self._uuid_generator_service.generate_uuid7()
