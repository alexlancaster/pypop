import base
import subprocess
import hashlib
import pytest
import os.path
import filecmp

def test_USAFEL():
    exit_code = base.run_pypop_process('./tests/data/minimal-no-emhaplofreq-no-guothompson.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = base.abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson.txt"))
    assert filecmp.cmp(out_filename, gold_out_filename)


@pytest.mark.xfail(reason="GuoThompson not yet functional in Python 3")
def test_USAFEL_guothompson():
    exit_code = base.run_pypop_process('./tests/data/minimal-no-emhaplofreq.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = base.abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq.txt"))
    assert filecmp.cmp(out_filename, gold_out_filename)

@pytest.mark.xfail(reason="Emhaplofreq not functional in Python 3")
def test_USAFEL_emhaplofreq():
    exit_code = base.run_pypop_process('./tests/data/minimal.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = base.abspath_test_data(os.path.join('./tests/data/output', out_filename))
    assert filecmp.cmp(out_filename, gold_out_filename)
