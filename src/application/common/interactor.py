"""Interactor base."""

from abc import abstractmethod
from typing import Any
from typing import Generic
from typing import TypeVar

RequestM = TypeVar("RequestM", bound=Any)
ResponseM = TypeVar("ResponseM", bound=Any)


class Interactor(Generic[RequestM, ResponseM]):
    """Base interactor class."""

    @abstractmethod
    async def __call__(
        self,
        request_model: RequestM,
    ) -> ResponseM:
        """Call an interactor."""
