"""Api key auth."""

from typing import TYPE_CHECKING
from typing import Any

from src.features.auth.security.api_key.config import ApiKeyAuth
from src.features.users.entities import User
from src.features.users.repositories.user import UserRepository

if TYPE_CHECKING:
    from litestar.connection import ASGIConnection


async def retrieve_user_handler(
    api_key: str,
    connection: "ASGIConnection[Any, Any, Any, Any]",
) -> User | None:
    """Retrieve a user from the token."""
    user_repository = await connection.state.dishka_container.get(UserRepository)
    return await user_repository.get_user_by_api_key(api_key)


api_key_auth = ApiKeyAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    exclude=["/docs"],
)
