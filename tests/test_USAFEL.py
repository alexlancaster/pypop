import sys
import subprocess
import hashlib
import pytest
import os.path
import filecmp
import difflib
from base import abspath_test_data, run_pypop_process, xfail_windows

def test_USAFEL():
    exit_code = run_pypop_process('./tests/data/minimal-no-emhaplofreq-no-guothompson-no-slatkin.ini', './tests/data/USAFEL-UchiTelle-small.pop', args=['-d'])
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson-no-slatkin.txt"))

    if sys.platform == "win32":
        diff = difflib.unified_diff(open(out_filename, 'r').readlines(), open(gold_out_filename, 'r').readlines())
        delta = ''.join(diff)
        print (delta)

        print(open("USAFEL-UchiTelle-small-out.xml").read())
    
    assert filecmp.cmp(out_filename, gold_out_filename)

@xfail_windows
def test_USAFEL_slatkin():
    exit_code = run_pypop_process('./tests/data/minimal-no-emhaplofreq-no-guothompson.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson.txt"))

    if sys.platform == "win32":
        diff = difflib.unified_diff(open(out_filename, 'r').readlines(), open(gold_out_filename, 'r').readlines())
        delta = ''.join(diff)
        print (delta)

    assert filecmp.cmp(out_filename, gold_out_filename)

@xfail_windows    
def test_USAFEL_slatkin_guothompson():
    exit_code = run_pypop_process('./tests/data/minimal-no-emhaplofreq.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq.txt"))
    assert filecmp.cmp(out_filename, gold_out_filename)

@xfail_windows    
def test_USAFEL_slatkin_guothompson_emhaplofreq():
    exit_code = run_pypop_process('./tests/data/minimal.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', out_filename))
    assert filecmp.cmp(out_filename, gold_out_filename)
