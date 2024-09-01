"""Persistence models for the auth feature."""

from datetime import UTC
from datetime import datetime

from advanced_alchemy.base import orm_registry
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy import UUID
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from uuid_utils import uuid7

from src.domain.entities.auth.api_key import ApiKey
from src.domain.entities.users.user import User

# Define the table for the ApiKey model
api_key_table = Table(
    # Table name
    "api_keys",
    # Metadata
    orm_registry.metadata,
    # Unique identifier for the user.
    Column("id", UUID, default=uuid7, primary_key=True, autoincrement=False),
    # Hash of the API key. Used for authentication.
    Column("key_hashed", String(128), nullable=False, unique=True, index=True),
    # Foreign key to the user the API key belongs to.
    Column("user_id", UUID, ForeignKey("users.id"), nullable=False, index=True),
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

# Map the ApiKey class to the api_key_table
orm_registry.map_imperatively(
    ApiKey,
    api_key_table,
    properties={
        "user": relationship(
            User,
            back_populates="api_keys",
        ),
    },
)
