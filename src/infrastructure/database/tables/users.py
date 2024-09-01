"""User model."""

from datetime import UTC
from datetime import datetime

from advanced_alchemy.base import orm_registry
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy import UUID
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from uuid_utils import uuid7

from src.domain.entities.auth.api_key import ApiKey
from src.domain.entities.users.user import User

# Define the table for the User model
user_table = Table(
    # Table name
    "users",
    # Metadata
    orm_registry.metadata,
    # Unique identifier for the user.
    Column("id", UUID, default=uuid7, primary_key=True, autoincrement=False),
    # Email address of the user.
    Column("email", String, nullable=False, unique=True),
    # Date/time of instance creation.
    Column(
        "created_at",
        DateTimeUTC(timezone=True),
        default=datetime.now(UTC),
        nullable=False,
    ),
    # Date/time of instance last update.
    Column(
        "updated_at",
        DateTimeUTC(timezone=True),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
        nullable=False,
    ),
)


# Map the User class to the user_table
orm_registry.map_imperatively(
    User,
    user_table,
    properties={
        "api_keys": relationship(ApiKey, back_populates="user"),
    },
)
