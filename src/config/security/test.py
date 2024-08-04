"""Security configuration for the application."""

from typing import Any

from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth
from litestar.security.jwt import Token

from src.config.settings import Settings
from src.features.users.entities import User


async def retrieve_user_handler(
    token: Token,
    connection: "ASGIConnection[Any, Any, Any, Any]",
) -> User | None:
    """Retrieve a user from the token."""
    print(111, token)
    # TODO: Implement logic to retrieve a user from the token.
    return User(id=1, email="admin@example.com")


settings = Settings()
jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.app.SECRET_KEY,
    exclude=["/login", "/docs"],
    # default_token_expiration=None,
)
