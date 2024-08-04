from typing import Any

from litestar.connection import ASGIConnection

from src.config.security.auth_api_key import ApiKeyAuth
from src.features.users.entities import User


async def retrieve_user_handler(
    # token: Token,
    connection: "ASGIConnection[Any, Any, Any, Any]",
) -> User | None:
    """Retrieve a user from the token."""
    print(111)
    # TODO: Implement logic to retrieve a user from the token.
    return User(id=1, email="admin@example.com")


api_key_auth = ApiKeyAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    # token_secret=settings.app.SECRET_KEY,
    exclude=["/login", "/docs"],
)
