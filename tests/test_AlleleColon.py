import subprocess
import hashlib
import pytest
from base import abspath_test_data, run_pypop_process, in_temp_dir

def test_AlleleColon_HardyWeinberg():
    exit_code = run_pypop_process('./tests/data/Test_Allele_Colon_HardyWeinberg.ini', './tests/data/Test_Allele_Colon_HardyWeinberg.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    with open("Test_Allele_Colon_HardyWeinberg-out.txt", 'rb') as out_handle:
        assert hashlib.md5(out_handle.read()).hexdigest() == 'aa0ad448139a3ea9c65ffa913ef97930'

def test_AlleleColon_Emhaplofreq():
    exit_code = run_pypop_process('./tests/data/Test_Allele_Colon_Emhaplofreq.ini', './tests/data/Test_Allele_Colon_Emhaplofreq.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    with open("Test_Allele_Colon_Emhaplofreq-out.txt", 'rb') as out_handle:
        assert hashlib.md5(out_handle.read()).hexdigest() == 'dc9b6530a8d85e0d4cf86cecf6b0a9c9'
