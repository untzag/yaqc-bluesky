__all__ = ["callbacks_before_func", "callbacks_after_func"]

import functools
from dataclasses import dataclass
from typing import List, Callable


callbacks_before_func: List[Callable[[FunctionArgs], None, None]] = []


callbacks_after_func: List[Callable[[FunctionResponse], None, None]]  = []


@dataclass
class FunctionArgs:
    name: str
    host: str
    port: int
    args: list
    kwargs: dict


@dataclass
class FunctionResponse:
    name: str
    host: str
    port: int
    data: object


def with_func_callbacks(func):

    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        for cb in callbacks_before_func:
            message = FunctionCallbackItem(func.__name__, self.yaq_client._host, self.yaq_client._port, args=args, kwargs=kwargs)
            cb(message)
        out = func(self, *args, **kwargs)
        for cb in callbacks_after_func:
            response = FunctionCallbackItem(func.__name__, self.yaq_client._host, self.yaq_client_port, out)
        return out

    return inner

