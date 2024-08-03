"""Base use case class."""

from abc import abstractmethod
from typing import Any
from typing import Generic
from typing import TypeVar

RequestM = TypeVar("RequestM", bound=Any)
ResponseM = TypeVar("ResponseM", bound=Any)


class UseCase(Generic[RequestM, ResponseM]):
    """Base use case class."""

    @abstractmethod
    async def __call__(
        self,
        request_model: RequestM,
        **kwargs,
    ) -> ResponseM:
        """Call a use case."""
