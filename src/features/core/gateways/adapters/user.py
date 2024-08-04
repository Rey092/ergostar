"""UserGatewayAdapter."""

from collections.abc import Sequence

from src.features.core.services.interfaces import ISeedManyEntries
from src.features.users.entities import User
from src.features.users.gateways import UserGateway


class UserGatewayAdapter(
    ISeedManyEntries[User],
):
    """UserGatewayAdapter."""

    def __init__(
        self,
        user_gateway: UserGateway,
    ):
        """Initialize gateway."""
        self._user_gateway = user_gateway

    async def add_many(
        self,
        data: list[User],
    ) -> Sequence[User]:
        """Add many entries."""
        return await self._user_gateway.add_many(data)

    async def delete_everything(self) -> None:
        """Delete all entries."""
        await self._user_gateway.delete_everything()

    async def exists_anything(self) -> bool:
        """Check if any entry exists."""
        return await self._user_gateway.exists_anything()
