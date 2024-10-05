"""Functions to handle providers"""

import importlib
import importlib.util
from typing import Callable, Any


def provider_is_valid(name: str) -> bool:
    """Check if `name` provider exists.

    The provider is given by a Python module inside aigor `providers` directory.
    It must contain a `run` function, that receives the string data from STDIN
    and return as string to be sent to STDOUT.

    Parameters
    ==========
    name : str
        Name of the provider.

    Returns
    ========
    bool
        If provider exists.
    """
    return importlib.util.find_spec(f"aigor.providers.{name}") is not None


def provider_get_func(name: str) -> Callable[..., Any] | Any | None:
    """Return a reference for provider function given the name.

    Parameters
    ===========
    name : str
        The name of the provider to look for

    Returns
    =======
    Callable | None
        Returns the function to provider or None on fail.
    """
    if provider_is_valid(name):
        module_name = f"aigor.providers.{name}"
        module = importlib.import_module(module_name)
        entrypoint = "run"
        func = getattr(module, entrypoint)
        if callable(func):
            return func

    return None


# def provider_call(name: str, args: dict | None) -> str:
#     """Call provider with `name` with `args`.
#     """
#     return ""
