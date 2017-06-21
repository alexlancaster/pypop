import subprocess
import hashlib
import pytest

def test_AlleleColon():
    process=subprocess.Popen(
        ['./bin/pypop.py', '-m', '-c', './data/ihiws2017/Test_Allele_Colon_HardyWeinberg.ini', './data/ihiws2017/Test_Allele_Colon_HardyWeinberg.pop'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    process.communicate()
    exit_code = process.wait()  # wait until script completed

    # check exit code
    assert exit_code == 0
    # compare with md5sum of output file
    assert hashlib.md5(open("Test_Allele_Colon_HardyWeinberg-out.txt", 'rb').read()).hexdigest() == 'ba0cd73c8ccd28fed726b0825688d620'

