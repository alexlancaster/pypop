import base
import subprocess
import hashlib
import pytest

def test_AlleleColon_HardyWeinberg():
    exit_code = base.run_pypop_process('./tests/data/Test_Allele_Colon_HardyWeinberg.ini', './tests/data/Test_Allele_Colon_HardyWeinberg.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_Allele_Colon_HardyWeinberg-out.txt", 'rb').read()).hexdigest() == '245a8a8493506c0b65ba9a3469173b13'

def test_AlleleColon_Emhaplofreq():
    
    exit_code = base.run_pypop_process('./tests/data/Test_Allele_Colon_Emhaplofreq.ini', './tests/data/Test_Allele_Colon_Emhaplofreq.pop')
    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_Allele_Colon_Emhaplofreq-out.txt", 'rb').read()).hexdigest() == '598954bfe301d5dea44ccd4d443905d1'
