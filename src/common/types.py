"""Common types for the project."""

from typing import TypeVar

from src.common.base.entity import Entity

EntityT = TypeVar("EntityT", bound=Entity)
