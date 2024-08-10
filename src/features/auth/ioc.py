"""Auth provider module."""

from dishka import AnyOf
from dishka import Provider
from dishka import Scope
from dishka import provide

from src.features.auth.interactors.create_api_key import CreateApiKeyInteractor
from src.features.auth.interactors.interfaces import ICreateApiKeyRepository
from src.features.auth.repositories.api_key import ApiKeyRepository


class AuthProvider(Provider):
    """Auth provider (DI)."""

    create_api_key_interactor = provide(
        source=CreateApiKeyInteractor,
        scope=Scope.REQUEST,
    )

    api_key_repository = provide(
        source=ApiKeyRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[ICreateApiKeyRepository],
    )
