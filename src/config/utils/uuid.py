"""UUID utility functions."""

from uuid_utils import uuid7


def generate_uuid7() -> str:
    """Generate UUID7 string."""
    return str(uuid7())
