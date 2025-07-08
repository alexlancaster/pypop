# add command-line option to pytest to skip certain tests
# provide an override to run them

# adapted from pytest documentation
# https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option

import os
from pathlib import Path

import pytest

# FIXME: a bit hacky
# set an environment variable for the current test directory
current_dir = Path(__file__).parent  # get the current test script directory
os.environ["PYPOP_CURRENT_TEST_DIRECTORY"] = str(current_dir)


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--pval-benchmarking",
        action="store_true",
        default=False,
        help="do pvalue benchmarking, requires scipy installed",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")
    config.addinivalue_line("markers", "pval_benchmarking: mark test as needing scipy")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--pval-benchmarking"):
        # FIXME: only check for SciPy if --pval-benchmarking is requested
        # so make this a lazy import
        import importlib.util  # noqa: PLC0415

        scipy_available = importlib.util.find_spec("scipy") is not None

        if not scipy_available:
            skip_pval = pytest.mark.skip(
                reason="scipy is required for --pval-benchmarking"
            )
        else:
            skip_pval = None
    else:
        skip_pval = pytest.mark.skip(reason="need --pval-benchmarking option to run")

    skip_slow = (
        None
        if config.getoption("--runslow")
        else pytest.mark.skip(reason="need --runslow option to run")
    )

    for item in items:
        if "slow" in item.keywords and skip_slow:
            item.add_marker(skip_slow)
        if "pval_benchmarking" in item.keywords and skip_pval:
            item.add_marker(skip_pval)
