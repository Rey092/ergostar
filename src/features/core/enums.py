"""Core application enums."""

from enum import Enum


class FixtureLoadingStrategy(Enum):
    """Fixture loading mode.

    Specifies how to load fixture data if data in the table already exists.

    ALLOW: Allow loading data
    SKIP: Skip loading data
    OVERRIDE: Override existing data
    RAISE: Raise an exception
    """

    ALLOW = "allow"
    SKIP = "skip"
    OVERRIDE = "override"
    RAISE = "raise"
