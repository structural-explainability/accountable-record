"""Smoke tests for the accountable_record package."""

from __future__ import annotations

import accountable_record


def test_package_imports() -> None:
    """The package can be imported."""
    assert accountable_record is not None
