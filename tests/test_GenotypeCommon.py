import base
import subprocess
import hashlib
import pytest

def test_GenotypeCommon_HardyWeinberg():
    exit_code = base.run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("BIGDAWG_SynthControl_Data-out.txt", 'rb').read()).hexdigest() == 'f0317091bfcc4cff28314be94f7e0649'

def test_GenotypeCommonDash_HardyWeinberg():
    exit_code = base.run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data_dash.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("BIGDAWG_SynthControl_Data_dash-out.txt", 'rb').read()).hexdigest() == '390f69633551352bbc4ee0c69355c6ad'
