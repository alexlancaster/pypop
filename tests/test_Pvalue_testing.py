# from base import abspath_test_data, run_pypop_process, filecmp_ignore_newlines, in_temp_dir, DEFAULT_GOLD_OUTPUT_DIR
from unittest import mock

import pytest

from PyPop.hardyweinberg import pval

chisq = 10.3
dof = 2
# expected = 0.0013303020906467733 for 1 dof
expected = 0.00579940472684215  # for 2 dof

pytestmark = (
    pytest.mark.pval_benchmarking
)  # applies the marker to all tests in this file


def test_SciPyPval(benchmark):
    # force using scipy
    with mock.patch("PyPop.hardyweinberg.use_scipy", True):
        result = benchmark(pval, chisq, dof)
        print(result)

    assert result == expected


def test_BuiltInPvalue(benchmark):
    result = benchmark(pval, chisq, dof)
    print(result)

    assert result == expected
