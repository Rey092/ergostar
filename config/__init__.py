"""Config module."""

from config.settings import Settings
from config import constants

settings = Settings()
__all__ = ["settings", "constants"]
