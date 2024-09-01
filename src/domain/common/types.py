"""Common types for the domain."""

from typing import TypeVar

from src.domain.common.entity import Entity

EntityT = TypeVar("EntityT", bound=Entity)
