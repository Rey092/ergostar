"""Auth Controller."""

from dishka import FromDishka
from litestar import Controller
from litestar import post

from src.features.auth.use_cases.create_api_key import CreateApiKeyRequestModel
from src.features.auth.use_cases.create_api_key import CreateApiKeyUseCase


class AuthController(Controller):
    """Auth Controller."""

    opt = {"exclude_from_auth": True}
    security = None

    @post("/create-api-key")
    async def create_api_key(
        self,
        create_api_key_use_case: FromDishka[CreateApiKeyUseCase],
    ) -> str:
        """Login."""
        return await create_api_key_use_case(
            CreateApiKeyRequestModel(
                user_id=1,
            )
        )
