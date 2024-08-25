"""Auth provider module."""

from dishka import AnyOf
from dishka import Provider
from dishka import Scope
from dishka import provide

from src.features.auth.interactors.authenticate import AuthenticateApiKeyInteractor
from src.features.auth.interactors.create_api_key import CreateApiKeyInteractor
from src.features.auth.interactors.get_user_api_keys import GetUserApiKeysInteractor
from src.features.auth.interfaces.hashers import IHasher
from src.features.auth.interfaces.hashers import IHashVerifier
from src.features.auth.interfaces.repositories import ICreateApiKeyRepository
from src.features.auth.interfaces.repositories import IGetAPIKeysAlchemyRepository
from src.features.auth.interfaces.repositories import IGetUserByApiKeyRepository
from src.features.auth.interfaces.services import IAddAPIKeyVaultRepository
from src.features.auth.interfaces.services import IAuthGenerateUUID7Service
from src.features.auth.interfaces.services import IGetAPIKeyListVaultRepository
from src.features.auth.repositories.a_user import AuthUserRepository
from src.features.auth.repositories.api_key import ApiKeyRepository
from src.features.auth.repositories.vault import ApiKeyVaultRepository
from src.features.auth.services.a_uuid_generator import AuthUUIDGeneratorAdapterService
from src.features.auth.services.hasher_blake2b import HasherBlake2b


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

    get_user_api_keys_interactor = provide(
        source=GetUserApiKeysInteractor,
        scope=Scope.REQUEST,
    )

    api_key_repository = provide(
        source=ApiKeyRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[ICreateApiKeyRepository, IGetAPIKeysAlchemyRepository],
    )

    auth_user_repository = provide(
        source=AuthUserRepository,
        scope=Scope.REQUEST,
        provides=IGetUserByApiKeyRepository,
    )

    vault_repository = provide(
        source=ApiKeyVaultRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[IGetAPIKeyListVaultRepository, IAddAPIKeyVaultRepository],
    )

    auth_generate_uuid7_service = provide(
        source=AuthUUIDGeneratorAdapterService,
        scope=Scope.APP,
        provides=IAuthGenerateUUID7Service,
    )

    hasher_service = provide(
        source=HasherBlake2b,
        scope=Scope.APP,
        provides=AnyOf[IHasher, IHashVerifier],
    )
