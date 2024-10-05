#!/usr/bin/env python
"""Simple provider for Aigor. Returns the same as input."""


def run(data: str) -> str:
    """Return input in output.

    Parameters
    ==========
    data : str
        Input data to provider

    Returns
    =======
    str
        Processed input.
    """
    result = "IDENTITY: " + data
    return result
