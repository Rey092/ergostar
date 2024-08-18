"""Common configuration for the application."""

from pydantic import BaseModel


class DTO(BaseModel):
    """Base DTO."""

    class Config:
        """Config."""

        from_attributes = True
