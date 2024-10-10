"""BaseComponentValueSetter class module."""

import inspect

__all__ = ["Callback"]


class Callback:
    """Callback class that saves a function and allows you to call it later."""

    def __init__(self, func):
        if not inspect.isroutine(func):
            raise ValueError(
                f"`func` must be a callable function, given: {func}"
            )
        self._func = func

    def __call__(self, *args, **kwargs):
        try:
            self._func(*args, **kwargs)
        except SystemExit:
            pass
