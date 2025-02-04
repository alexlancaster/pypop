import hashlib
import pytest
from unittest import mock
from base import (
    in_temp_dir,  # noqa: F401
    run_pypop_process,
)

def test_GenotypeCommon_HardyWeinberg_scipy_pval(benchmark):

    with mock.patch('PyPop.HardyWeinberg.use_scipy', True) as new_scipy:    
        exit_code = benchmark(run_pypop_process, './tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data.pop')
        
        # check exit code
        assert exit_code == 0
        # compare with md5sum of output file
        with open("BIGDAWG_SynthControl_Data-out.txt", 'rb') as out_handle:
            assert hashlib.md5(out_handle.read()).hexdigest() == '7162aa0715ccfd1cb7b666409d839129'

def test_GenotypeCommon_HardyWeinberg_compiled_pval(benchmark):
    exit_code = benchmark(run_pypop_process, './tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    with open("BIGDAWG_SynthControl_Data-out.txt", 'rb') as out_handle:
        assert hashlib.md5(out_handle.read()).hexdigest() == '7162aa0715ccfd1cb7b666409d839129'
        


def test_GenotypeCommon_HardyWeinberg():
    exit_code = run_pypop_process(
        "./tests/data/WS_BDCtrl_Test_HW.ini",
        "./tests/data/BIGDAWG_SynthControl_Data.pop",
    )
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    with open("BIGDAWG_SynthControl_Data-out.txt", "rb") as out_handle:
        assert (
            hashlib.md5(out_handle.read()).hexdigest()
            == "099138eb81d9fd1ef8a3e9cde8fa1e60"
        )


def test_GenotypeCommonDash_HardyWeinberg():
    exit_code = run_pypop_process(
        "./tests/data/WS_BDCtrl_Test_HW.ini",
        "./tests/data/BIGDAWG_SynthControl_Data_dash.pop",
    )
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    with open("BIGDAWG_SynthControl_Data_dash-out.txt", "rb") as out_handle:
        assert (
            hashlib.md5(out_handle.read()).hexdigest()
            == "5e641d6245388e257f62843963eb1aa3"
        )
