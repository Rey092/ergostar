"""Enums for the core module."""

from enum import Enum


class DatabaseSeedingGroups(str, Enum):
    """Database seeding groups."""

    subscriptions = "subscriptions"
