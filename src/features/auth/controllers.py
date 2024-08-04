"""Auth Controller."""

from typing import Any

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller
from litestar import Request
from litestar import post

from src.features.auth.use_cases.create_api_key import CreateApiKeyRequestModel
from src.features.auth.use_cases.create_api_key import CreateApiKeyUseCase
from src.features.users.entities import User


class AuthController(Controller):
    """Auth Controller."""

    @post("/create-api-key", opt={"exclude_from_auth": True}, security=[{}])
    @inject
    async def create_api_key(
        self,
        create_api_key_use_case: FromDishka[CreateApiKeyUseCase],
    ) -> str:
        """Create an api key. Exclude from auth."""
        return await create_api_key_use_case(
            CreateApiKeyRequestModel(
                user_id=1,
            ),
        )

    @post("/check-auth")
    @inject
    async def check_auth(
        self,
        request: Request[User, str, Any],
    ) -> dict:
        """Test auth."""
        return {
            "user_id": request.user.id,
            "email": request.user.email,
            "api_key": request.auth,
        }
