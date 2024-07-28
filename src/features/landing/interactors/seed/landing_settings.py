"""Seed landing settings interactor."""
import logging

from src.common.interfaces.db import IDatabaseSession
from src.features.core.services.fixture_loader import FixtureLoaderService
from src.features.landing import LandingSettings
from src.features.landing.interactors.seed import interfaces

logger = logging.getLogger(__name__)


class SeedLandingSettingsInteractor:
    """Seed landing settings interactor."""

    def __init__(
        self,
        session: IDatabaseSession,
        landing_settings_repository: interfaces.ISeedLandingSettings,
        fixture_loader_service: FixtureLoaderService,
    ):
        """Initialize interactor."""
        self._session = session
        self._landing_settings_repository = landing_settings_repository
        self._fixture_loader_service = fixture_loader_service

    async def __call__(self) -> None:
        """
        Seed landing settings.

        Return landing settings if created.
        """

        # check if landing settings exist
        if await self._landing_settings_repository.exists():
            logger.info("Landing settings already exist.")
            return

        # load landing settings fixture
        entities: list[LandingSettings] = await self._fixture_loader_service.load_fixture_to_entity(
            future_name="landing",
            fixture_name="landing_settings",
            entity_class=LandingSettings
        )

        if len(entities) == 0:
            logger.info("No landing settings fixtures found.")
            return

        if len(entities) > 1:
            logger.warning("Multiple landing settings fixtures found. Using the first one.")

        # get the first entity
        entity: LandingSettings = entities[0]

        # add landing settings
        await self._landing_settings_repository.add(obj=entity)

        # commit LandingSettings
        await self._session.commit()

        logger.info("Landing settings seeded.")
