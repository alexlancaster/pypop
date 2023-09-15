import subprocess
import hashlib
import pytest
from base import abspath_test_data, run_pypop_process, xfail_windows, in_temp_dir

def test_GenotypeCommon_HardyWeinberg():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("BIGDAWG_SynthControl_Data-out.txt", 'rb').read()).hexdigest() == 'db4bc1113e9eab337561f7510e73381f'

def test_GenotypeCommonDash_HardyWeinberg():
    exit_code = run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data_dash.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("BIGDAWG_SynthControl_Data_dash-out.txt", 'rb').read()).hexdigest() == '36053392f9dd25c9a2a6bb1fc6db242a'
