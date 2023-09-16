import sys
import subprocess
import hashlib
import pytest
import os.path
from base import abspath_test_data, run_pypop_process, xfail_windows, filecmp_ignore_newlines, in_temp_dir

def test_USAFEL():
    exit_code = run_pypop_process('./tests/data/minimal-no-emhaplofreq-no-guothompson-no-slatkin.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson-no-slatkin.txt"))

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

def test_USAFEL_slatkin():
    exit_code = run_pypop_process('./tests/data/minimal-no-emhaplofreq-no-guothompson.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson.txt"))

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

def test_USAFEL_slatkin_guothompson():
    exit_code = run_pypop_process('./tests/data/minimal-no-emhaplofreq.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq.txt"))
    assert filecmp_ignore_newlines(out_filename, gold_out_filename)

@xfail_windows    
def test_USAFEL_slatkin_guothompson_emhaplofreq():
    exit_code = run_pypop_process('./tests/data/minimal.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', out_filename))
    assert filecmp_ignore_newlines(out_filename, gold_out_filename)
