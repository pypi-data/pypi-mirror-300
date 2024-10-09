from collections.abc import Awaitable, Callable
from typing import Protocol, TypeAlias, runtime_checkable

from asgikit.requests import Request

__all__ = ("Middleware", "CallNext")


CallNext: TypeAlias = Callable[[Request], Awaitable]


@runtime_checkable
class Middleware(Protocol):
    async def __call__(
        self,
        call_next: CallNext,
        request: Request,
    ):
        raise NotImplementedError()
