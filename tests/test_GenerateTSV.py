import base
import subprocess
import hashlib
import pytest

def test_GenerateTSV():
    exit_code = base.run_pypop_process('./tests/data/WS_BDCtrl_Test_HW.ini', './tests/data/BIGDAWG_SynthControl_Data.pop', args=['--generate-tsv'])
    # check exit code
    assert exit_code == 0
    # compare with output files
    # FIXME: not yet implemented
