"""Api key auth."""

from typing import TYPE_CHECKING
from typing import Any

from src.application.interactors.auth.authenticate import AuthenticateApiKeyInteractor
from src.application.interactors.auth.authenticate import AuthenticateApiKeyRequestModel
from src.domain.entities.users.user import User
from src.infrastructure.security.api_key.config import ApiKeyAuth

if TYPE_CHECKING:
    from litestar.connection import ASGIConnection


async def retrieve_user_handler(
    api_key: str,
    connection: "ASGIConnection[Any, Any, Any, Any]",
) -> User:
    """Retrieve a user from the token."""
    interactor: AuthenticateApiKeyInteractor = (
        await connection.state.dishka_container.get(AuthenticateApiKeyInteractor)
    )
    return await interactor(
        request_model=AuthenticateApiKeyRequestModel(api_key=api_key),
    )


api_key_auth = ApiKeyAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    exclude=["/docs"],
)
