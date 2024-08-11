"""Repository interface."""

from advanced_alchemy.repository import ModelT

from src.common.interfaces.mapper import IMapper
from src.common.types import EntityT


class IRepository(
    IMapper[EntityT, ModelT],
):
    """Repository interface."""
