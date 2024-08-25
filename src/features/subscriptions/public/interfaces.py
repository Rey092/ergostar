"""Public interfaces for the subscriptions feature."""

from typing import Protocol

from src.common.base.repositories.alchemy import IGenericRepositoryProtocol
from src.common.interfaces.fixture_loader.repository import ISeedRepository
from src.common.types import EntityT


class ISubscriptionPlanRepositoryContract(
    ISeedRepository[EntityT],
    IGenericRepositoryProtocol[EntityT],
    Protocol[EntityT],
):
    """ISubscriptionPlanSeedManyEntries."""
