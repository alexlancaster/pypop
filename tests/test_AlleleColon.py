import base
import subprocess
import hashlib
import pytest

def test_AlleleColon_HardyWeinberg():
    process=subprocess.Popen(
        ['./bin/pypop.py', '-m', '-c', './tests/data/Test_Allele_Colon_HardyWeinberg.ini', './tests/data/Test_Allele_Colon_HardyWeinberg.pop'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    process.communicate()
    exit_code = process.wait()  # wait until script completed

    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_Allele_Colon_HardyWeinberg-out.txt", 'rb').read()).hexdigest() == '9328d297f91a926b6db44a4bd0c90f55'


def test_AlleleColon_Emhaplofreq():
    process=subprocess.Popen(
        ['./bin/pypop.py', '-m', '-c', './tests/data/Test_Allele_Colon_Emhaplofreq.ini', './tests/data/Test_Allele_Colon_Emhaplofreq.pop'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    process.communicate()
    exit_code = process.wait()  # wait until script completed

    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_Allele_Colon_Emhaplofreq-out.txt", 'rb').read()).hexdigest() == '4fb4b5c74f9b1c6a0f686200e3cd543a'
