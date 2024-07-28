"""Entity interface."""
import datetime
from typing import Any, TypeVar
from dataclasses import asdict, dataclass, fields
from sqlalchemy import FromClause
from sqlalchemy.orm import Mapper

T = TypeVar('T', bound='Entity')


class Entity:
    """Entity"""

    __table__: FromClause
    __mapper__: Mapper[Any]
    __name__: str

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        """
        Convert entity to dictionary.

        Returns:
            dict[str, Any]: A dict representation of the entity
        """
        self: dataclass
        if exclude is None:
            exclude = set()
        return {k: v for k, v in asdict(self).items() if k not in exclude}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> T:
        """
        Update entity from dictionary.

        Args:
            data (dict[str, Any]): Dictionary to update entity from
        """
        cls: dataclass
        field_types = {f.name: f.type for f in fields(cls)}
        return cls(**{k: cls._convert_type(field_types[k], v) for k, v in data.items()})

    @staticmethod
    def _convert_type(field_type: Any, value: Any) -> Any:
        """
        Convert value to the specified field type.

        Args:
            field_type (Any): The type to convert the value to
            value (Any): The value to convert

        Returns:
            Any: The converted value
        """
        try:
            if field_type is datetime.datetime:
                return datetime.datetime.fromisoformat(value).replace(tzinfo=None)
            return field_type(value)
        except (TypeError, ValueError) as e:
            return value
