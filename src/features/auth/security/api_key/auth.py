"""Api key auth."""

from typing import TYPE_CHECKING
from typing import Any

from src.features.auth.interactors.authenticate import AuthenticateApiKeyInteractor
from src.features.auth.interactors.authenticate import AuthenticateApiKeyRequestModel
from src.features.auth.security.api_key.config import ApiKeyAuth
from src.features.users.public.entities.user import UserEntity

if TYPE_CHECKING:
    from litestar.connection import ASGIConnection


async def retrieve_user_handler(
    api_key: str,
    connection: "ASGIConnection[Any, Any, Any, Any]",
) -> UserEntity:
    """Retrieve a user from the token."""
    interactor: AuthenticateApiKeyInteractor = (
        await connection.state.dishka_container.get(AuthenticateApiKeyInteractor)
    )
    return await interactor(
        request_model=AuthenticateApiKeyRequestModel(api_key=api_key),
    )


api_key_auth = ApiKeyAuth[UserEntity](
    retrieve_user_handler=retrieve_user_handler,
    exclude=["/docs"],
)
