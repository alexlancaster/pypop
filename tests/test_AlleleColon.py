import subprocess
import hashlib
import pytest
from base import abspath_test_data, run_pypop_process, xfail_windows, in_temp_dir

def test_AlleleColon_HardyWeinberg():
    exit_code = run_pypop_process('./tests/data/Test_Allele_Colon_HardyWeinberg.ini', './tests/data/Test_Allele_Colon_HardyWeinberg.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_Allele_Colon_HardyWeinberg-out.txt", 'rb').read()).hexdigest() == '245a8a8493506c0b65ba9a3469173b13'

def test_AlleleColon_Emhaplofreq():
    exit_code = run_pypop_process('./tests/data/Test_Allele_Colon_Emhaplofreq.ini', './tests/data/Test_Allele_Colon_Emhaplofreq.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_Allele_Colon_Emhaplofreq-out.txt", 'rb').read()).hexdigest() == 'dc9b6530a8d85e0d4cf86cecf6b0a9c9'
