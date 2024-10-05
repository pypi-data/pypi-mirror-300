#!/usr/bin/env python
"""Tests for identity provider"""

from aigor.providers.identity import run


def test_identity() -> None:
    value: str = "x"
    assert run(f"{value}") == f"IDENTITY: {value}"
