import base
import subprocess
import hashlib
import pytest

def test_GenotypeCommon_HardyWeinberg():
    exit_code = base.run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("BIGDAWG_SynthControl_Data-out.txt", 'rb').read()).hexdigest() == 'c0f35b5b30ed20211fd37ff0a6021061'

def test_GenotypeCommonDash_HardyWeinberg():
    exit_code = base.run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data_dash.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("BIGDAWG_SynthControl_Data_dash-out.txt", 'rb').read()).hexdigest() == '7dce2213b3ec0109ed232b40d71ad961'
