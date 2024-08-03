"""Entity interface."""

import datetime
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import fields
from typing import Any
from typing import Self


@dataclass()
class Entity:
    """Entity."""

    __name__: str

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        """Convert entity to dictionary.

        Returns:
        -------
            dict[str, Any]: A dict representation of the entity
        z

        """
        if exclude is None:
            exclude = set()
        return {k: v for k, v in asdict(self).items() if k not in exclude}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Update entity from dictionary.

        Args:
        ----
            data (dict[str, Any]): Dictionary to update entity from

        """
        field_types = {f.name: f.type for f in fields(cls)}
        return cls(
            **{k: cls._convert_type(field_types[k], v) for k, v in data.items()},
        )

    @staticmethod
    def _convert_type(field_type: Any, value: Any) -> Any:
        """Convert value to the specified field type.

        Args:
        ----
            field_type (Any): The type to convert the value to
            value (Any): The value to convert

        Returns:
        -------
            Any: The converted value

        """
        try:
            if field_type is datetime.datetime:
                return datetime.datetime.fromisoformat(value).replace(
                    tzinfo=None,
                )
            return field_type(value)
        except (TypeError, ValueError):
            return value
