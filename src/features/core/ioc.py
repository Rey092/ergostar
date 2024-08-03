"""Core provider module."""

from dishka import Provider
from dishka import Scope
from dishka import provide

from src.features.core.interactors.drop_database import DropDatabaseInteractor
from src.features.core.interactors.seed_database import SeedDatabaseInteractor
from src.features.core.services.fixture_loader import FixtureLoaderService


class CoreProvider(Provider):
    """Core provider (DI)."""

    drop_database_interactor = provide(
        source=DropDatabaseInteractor,
        scope=Scope.REQUEST,
    )

    seed_database_interactor = provide(
        source=SeedDatabaseInteractor,
        scope=Scope.REQUEST,
    )

    fixture_loader_service = provide(
        source=FixtureLoaderService,
        scope=Scope.REQUEST,
    )
