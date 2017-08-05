import base
import subprocess
import hashlib
import pytest
import os.path
import filecmp

def test_USAFEL():
    exit_code = base.run_pypop_process('./tests/data/minimal.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = os.path.join('./tests/data/output', out_filename)
    assert filecmp.cmp(out_filename, gold_out_filename)
