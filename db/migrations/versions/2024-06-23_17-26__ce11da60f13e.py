# type: ignore
"""

Revision ID: ce11da60f13e
Revises: 8b7e9c4d5449
Create Date: 2024-06-23 17:26:42.333355+00:00

"""
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from advanced_alchemy.types import EncryptedString, EncryptedText, GUID, ORA_JSONB, DateTimeUTC
from sqlalchemy import Text  # noqa: F401

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = ["downgrade", "upgrade", "schema_upgrades", "schema_downgrades", "data_upgrades", "data_downgrades"]

sa.GUID = GUID
sa.DateTimeUTC = DateTimeUTC
sa.ORA_JSONB = ORA_JSONB
sa.EncryptedString = EncryptedString
sa.EncryptedText = EncryptedText

# revision identifiers, used by Alembic.
revision = 'ce11da60f13e'
down_revision = '8b7e9c4d5449'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            schema_upgrades()
            data_upgrades()

def downgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            data_downgrades()
            schema_downgrades()

def schema_upgrades() -> None:
    """schema upgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('landing__snippet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feather_icon', sa.String(length=40), nullable=True))

    # ### end Alembic commands ###

def schema_downgrades() -> None:
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('landing__snippet', schema=None) as batch_op:
        batch_op.drop_column('feather_icon')

    # ### end Alembic commands ###

def data_upgrades() -> None:
    """Add any optional data upgrade migrations here!"""

def data_downgrades() -> None:
    """Add any optional data downgrade migrations here!"""
