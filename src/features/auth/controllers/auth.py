"""Auth Controller."""

from typing import Any
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller
from litestar import Request
from litestar import post

from src.features.auth.interactors.create_api_key import CreateApiKeyInteractor
from src.features.auth.interactors.create_api_key import CreateApiKeyRequestModel
from src.features.auth.interfaces.services import IGetAPIKeyListVaultRepository
from src.features.users.entities.user import User


class AuthController(Controller):
    """Auth Controller."""

    @post("/create-api-key", opt={"exclude_from_auth": True}, security=[{}])
    @inject
    async def create_api_key(
        self,
        interactor: FromDishka[CreateApiKeyInteractor],
    ) -> str:
        """Create an api key. Exclude from auth."""
        return await interactor(
            CreateApiKeyRequestModel(
                user_id=UUID("3165d5df-17a7-4562-b5f5-5f4bd16c97f3"),
            ),
        )

    @post("/check-auth")
    @inject
    async def check_auth(
        self,
        request: Request[User, str, Any],
        vault_repository: FromDishka[IGetAPIKeyListVaultRepository],
    ) -> dict:
        """Test auth."""
        return {
            "user_id": request.user.id,
            "email": request.user.email,
            "token": request.auth,
            "api_keys": await vault_repository.get_user_api_keys(
                user_id=request.user.id,
            ),
        }
