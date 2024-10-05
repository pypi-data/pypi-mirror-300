"""AIgor is an assistant for oldschool unix users."""

from typing import Any
from aigor.state_manager import _StateManager

__appname__ = "aigor"
__appauthor__ = "morgado"
__version__ = "0.0.3"


# Create a singleton instance
_state_manager = _StateManager()


# Public interface
def state_get(key: str, default: Any | None = None) -> Any:
    """Get `key` state.

    Parameters
    ==========
    key : str
        State to get.
    default : Any | None
        If key is missing returns `default` value.

    Returns
    ========
    Any
        Value of the state `key`.
    """
    return _state_manager.get(key, default)


def state_set(key: str, value: Any) -> None:
    """Set `key` state with value.

    Parameters
    ==========
    key : str
        State to get.
    value : Any
        Value of the state `key`.
    """
    _state_manager.set(key, value)


def state_delete(key: str) -> None:
    """Delete `key` from global state.

    Parameters
    ==========
    key : str
        State to get.
    """
    _state_manager.delete(key)


def state_clear() -> None:
    """Delete all keys from global state."""
    _state_manager.clear()


def state_get_full() -> dict[str, Any]:
    """Get the global state dictionary"""
    return _state_manager.state
