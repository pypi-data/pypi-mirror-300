"""Defines the state manager."""

from typing import Any, Self


class _StateManager:
    """Defines a singleton state manager."""

    def __init__(self) -> None:
        """Initializes an empty state.
        self : Self
            The object instance.
        """
        self._state: dict[str, Any] = {}

    def get(self: Self, key: str, default: Any | None = None) -> Any:
        """Get `key` state.

        Parameters
        ==========
        key : str
            State to get.

        Returns
        ========
        Any
            Value of the state `key`.
        """
        return self._state.get(key, default)

    def set(self: Self, key: str, value: Any) -> None:
        """Set `key` state with value.

        Parameters
        ==========
        key : str
            State to get.
        value : Any
            Value of the state `key`.
        """
        self._state[key] = value

    def delete(self: Self, key: str) -> None:
        """Delete `key` from global state.

        Parameters
        ==========
        key : str
            State to get.
        """
        self._state.pop(key, None)

    def clear(self: Self) -> None:
        """Delete all keys from global state."""
        self._state.clear()

    @property
    def state(self: Self) -> dict[str, Any]:
        """Get the global state dictionary

        Returns
        =======
        dict[str, Any]
            Global state dictionary
        """
        return self._state
