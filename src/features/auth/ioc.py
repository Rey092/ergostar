"""Auth provider module."""

from dishka import AnyOf
from dishka import Provider
from dishka import Scope
from dishka import provide

from src.features.auth.interactors.authenticate import AuthenticateApiKeyInteractor
from src.features.auth.interactors.create_api_key import CreateApiKeyInteractor
from src.features.auth.interfaces.hashers import IHasher
from src.features.auth.interfaces.hashers import IHashVerifier
from src.features.auth.interfaces.repositories import ICreateApiKeyRepository
from src.features.auth.interfaces.repositories import IGetAPIKeysRepository
from src.features.auth.interfaces.repositories import IGetUserByApiKeyRepository
from src.features.auth.interfaces.services import IAddAPIKeyVaultService
from src.features.auth.interfaces.services import IGenerateUUID7Service
from src.features.auth.interfaces.services import IGetAPIKeyListVaultService
from src.features.auth.repositories.a_user import AuthUserAdapterRepository
from src.features.auth.repositories.api_key import ApiKeyRepository
from src.features.auth.services.a_uuid_generator import AuthUUIDGeneratorAdapterService
from src.features.auth.services.hasher_blake2b import HasherBlake2b
from src.features.auth.services.vault import VaultService


class AuthProvider(Provider):
    """Auth provider (DI)."""

    authenticate_api_key_interactor = provide(
        source=AuthenticateApiKeyInteractor,
        scope=Scope.REQUEST,
    )

    create_api_key_interactor = provide(
        source=CreateApiKeyInteractor,
        scope=Scope.REQUEST,
    )

    api_key_repository = provide(
        source=ApiKeyRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[ICreateApiKeyRepository, IGetAPIKeysRepository],
    )

    auth_user_repository = provide(
        source=AuthUserAdapterRepository,
        scope=Scope.REQUEST,
        provides=IGetUserByApiKeyRepository,
    )

    auth_generate_uuid7_service = provide(
        source=AuthUUIDGeneratorAdapterService,
        scope=Scope.APP,
        provides=IGenerateUUID7Service,
    )

    hasher_service = provide(
        source=HasherBlake2b,
        scope=Scope.APP,
        provides=AnyOf[IHasher, IHashVerifier],
    )

    vault_service = provide(
        source=VaultService,
        scope=Scope.REQUEST,
        provides=AnyOf[IGetAPIKeyListVaultService, IAddAPIKeyVaultService],
    )
