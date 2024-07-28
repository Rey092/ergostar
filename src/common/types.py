"""Common types for the project."""
from typing import TypeVar

SETTINGS_DEBUG = TypeVar("SETTINGS_DEBUG", bound=bool)
SETTINGS_FEATURES_PATH = TypeVar("SETTINGS_FEATURES_PATH", bound=str)
