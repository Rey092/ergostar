"""Auth Controller."""

from typing import Any
from uuid import UUID

from cashews import cache
from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller
from litestar import Request
from litestar import post

from src.features.auth.dtos.api_keys import GetUserApiKeysDTO
from src.features.auth.interactors.create_api_key import CreateApiKeyInteractor
from src.features.auth.interactors.create_api_key import CreateApiKeyRequestModel
from src.features.auth.interactors.get_user_api_keys import GetUserApiKeysInteractor
from src.features.auth.interactors.get_user_api_keys import GetUserApiKeysRequestModel
from src.features.users.public.entities.user import UserEntity


class AuthController(Controller):
    """Auth Controller."""

    @post("/create-api-key", opt={"exclude_from_auth": True}, security=[{}])
    @inject
    @cache.rate_limit(
        limit=1,
        period="2s",
        key="create_api_key:3165d5df-17a7-4562-b5f5-5f4bd16c97f3",
    )
    async def create_api_key(
        self,
        interactor: FromDishka[CreateApiKeyInteractor],
    ) -> UUID:
        """Create an api key.

        Excluded from auth.

        Rate limit: One request per 2 seconds.
        Rate limit is used to prevent spam and race conditions.
        """
        return await interactor(
            CreateApiKeyRequestModel(
                user_id=UUID("3165d5df-17a7-4562-b5f5-5f4bd16c97f3"),
            ),
        )

    @post("/check-auth")
    @inject
    async def check_auth(
        self,
        request: Request[UserEntity, str, Any],
        interactor: FromDishka[GetUserApiKeysInteractor],
    ) -> GetUserApiKeysDTO:
        """Test auth."""
        response_model = await interactor(
            GetUserApiKeysRequestModel(
                user_id=UUID(str(request.user.id)),
            ),
        )
        return GetUserApiKeysDTO.model_validate(response_model)
