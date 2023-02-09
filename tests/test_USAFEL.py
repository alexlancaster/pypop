import base
import subprocess
import hashlib
import pytest
import os.path
import filecmp
import difflib

def test_USAFEL():
    exit_code = base.run_pypop_process('./tests/data/minimal-no-emhaplofreq-no-guothompson-no-slatkin.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = base.abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson-no-slatkin.txt"))

    diff = difflib.unified_diff(open(out_filename, 'r').readlines(), open(gold_out_filename, 'r').readlines())
    delta = ''.join(diff)
    print (delta)

    assert filecmp.cmp(out_filename, gold_out_filename)


def test_USAFEL_slatkin():
    exit_code = base.run_pypop_process('./tests/data/minimal-no-emhaplofreq-no-guothompson.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = base.abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq-noguothompson.txt"))

    diff = difflib.unified_diff(open(out_filename, 'r').readlines(), open(gold_out_filename, 'r').readlines())
    delta = ''.join(diff)
    print (delta)

    assert filecmp.cmp(out_filename, gold_out_filename)

def test_USAFEL_slatkin_guothompson():
    exit_code = base.run_pypop_process('./tests/data/minimal-no-emhaplofreq.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = base.abspath_test_data(os.path.join('./tests/data/output', "USAFEL-UchiTelle-small-out-no-emhaplofreq.txt"))
    assert filecmp.cmp(out_filename, gold_out_filename)

def test_USAFEL_slatkin_guothompson_emhaplofreq():
    exit_code = base.run_pypop_process('./tests/data/minimal.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-out.txt"
    gold_out_filename = base.abspath_test_data(os.path.join('./tests/data/output', out_filename))
    assert filecmp.cmp(out_filename, gold_out_filename)
