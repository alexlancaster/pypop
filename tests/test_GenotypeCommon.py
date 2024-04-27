import subprocess
import hashlib
import pytest
from base import abspath_test_data, run_pypop_process, in_temp_dir

def test_GenotypeCommon_HardyWeinberg():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    with open("BIGDAWG_SynthControl_Data-out.txt", 'rb') as out_handle:
        assert hashlib.md5(out_handle.read()).hexdigest() == '7162aa0715ccfd1cb7b666409d839129'

def test_GenotypeCommonDash_HardyWeinberg():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data_dash.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    with open("BIGDAWG_SynthControl_Data_dash-out.txt", 'rb') as out_handle:
        assert hashlib.md5(out_handle.read()).hexdigest() == 'ee7d37fb5a21419d917bf343f2315083'
