import base
import subprocess
import hashlib
import pytest

def test_AlleleColon_HardyWeinberg():
    exit_code = base.run_pypop_process('./tests/data/Test_Allele_Colon_HardyWeinberg.ini', './tests/data/Test_Allele_Colon_HardyWeinberg.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_Allele_Colon_HardyWeinberg-out.txt", 'rb').read()).hexdigest() == '3b4fef611f7a5897cc649b6bb5bbbcda'

def test_AlleleColon_Emhaplofreq():
    
    exit_code = base.run_pypop_process('./tests/data/Test_Allele_Colon_Emhaplofreq.ini', './tests/data/Test_Allele_Colon_Emhaplofreq.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_Allele_Colon_Emhaplofreq-out.txt", 'rb').read()).hexdigest() == 'c262cf621f18e53895d3522e90c3804b'
