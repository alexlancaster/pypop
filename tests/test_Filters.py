import sys
import subprocess
import hashlib
import pytest
import os.path
from base import abspath_test_data, run_pypop_process, xfail_windows, filecmp_ignore_newlines

def test_Filters_DigitBinning_USAFEL():
    exit_code = run_pypop_process('./tests/data/Filters_DigitBinning_USAFEL.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-Filters_DigitBinning-out.txt"
    gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', out_filename))

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)


def test_Filters_CustomBinning_USAFEL():
    exit_code = run_pypop_process('./tests/data/Filters_CustomBinning_USAFEL.ini', './tests/data/USAFEL-UchiTelle-small.pop')
    # check exit code
    assert exit_code == 0

    out_filename = "USAFEL-UchiTelle-small-Filters_CustomBinning-out.txt"
    gold_out_filename = abspath_test_data(os.path.join('./tests/data/output', out_filename))

    assert filecmp_ignore_newlines(out_filename, gold_out_filename)
    
