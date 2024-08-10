"""Generic repository class for SQLAlchemy."""

from advanced_alchemy.repository import ModelT
from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository
from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepositoryProtocol


class GenericSQLAlchemyRepositoryProtocol(
    SQLAlchemyAsyncSlugRepositoryProtocol[ModelT],
):
    """Generic repository protocol for SQLAlchemy."""


class GenericSQLAlchemyRepository(
    SQLAlchemyAsyncSlugRepository[ModelT],
    GenericSQLAlchemyRepositoryProtocol[ModelT],
):
    """Generic repository for SQLAlchemy."""
