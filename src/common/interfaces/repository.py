"""Repository interface."""

from sqlalchemy.ext.asyncio import AsyncSession


class IRepository:
    """Repository interface."""

    _session: AsyncSession
