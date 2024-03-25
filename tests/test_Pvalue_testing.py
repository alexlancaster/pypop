import pytest
#from base import abspath_test_data, run_pypop_process, filecmp_ignore_newlines, in_temp_dir, DEFAULT_GOLD_OUTPUT_DIR
from unittest import mock

chisq = 10.3
dof = 2
#expected = 0.0013303020906467733 for 1 dof
expected = 0.00579940472684215  # for 2 dof

def test_SciPyPval(benchmark):

    # force using scipy
    with mock.patch('PyPop.HardyWeinberg.use_scipy', True) as new_scipy:
        from PyPop.HardyWeinberg import pval
        result = benchmark(pval, chisq, dof)
        print(result)

    assert result == expected    

def test_BuiltInPvalue(benchmark):

    from PyPop.HardyWeinberg import pval
    result = benchmark(pval, chisq, dof)
    print(result)
    
    assert result == expected

        
