"""DTOs for api keys."""

from datetime import datetime
from uuid import UUID

from src.common.base.dto import DTO


class ApiKeyDTO(DTO):
    """Api key DTO."""

    api_key_id: UUID
    api_key_value: UUID | None
    date_created: datetime


class GetUserApiKeysDTO(DTO):
    """Get user api keys response model."""

    user_id: UUID
    api_keys: list[ApiKeyDTO]
