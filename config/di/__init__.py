"""Dependency injection module."""
from src.landing.provider import LandingProvider
from .postgres import PostgresProvider
from src.subscriptions.provider import SubscriptionProvider

__all__ = [
    "LandingProvider",
    "PostgresProvider",
    "SubscriptionProvider",
]
