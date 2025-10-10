"""Logic to skip doctests in .rst files based on Python version."""

import sys

import pytest


def pytest_collection_modifyitems(config, items):  # noqa: ARG001
    """Skip tests for website rst in Python < 3.9."""
    if sys.version_info < (3, 9):
        skip = pytest.mark.skip(
            reason="requires importlib.resources.files (Python ≥ 3.9)"
        )
        for item in items:
            if "guide-chapter-usage.rst" in str(item.fspath):
                item.add_marker(skip)
