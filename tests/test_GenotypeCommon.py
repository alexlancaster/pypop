import base
import subprocess
import hashlib
import pytest

def test_GenotypeCommon_HardyWeinberg():
    exit_code = base.run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("BIGDAWG_SynthControl_Data-out.txt", 'rb').read()).hexdigest() == '276263b0d0d9fc03b77826388d70510d'

def test_GenotypeCommonDash_HardyWeinberg():
    exit_code = base.run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data_dash.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("BIGDAWG_SynthControl_Data_dash-out.txt", 'rb').read()).hexdigest() == 'b0f4247a2a67a65d0109b6448427cc28'
